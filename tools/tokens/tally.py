#!/usr/bin/env python3
"""Aggregate token usage from local Claude Code and Codex transcripts."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, time
from pathlib import Path
from typing import Iterable, Iterator, Optional, Sequence


TOKEN_FIELDS = ("input_tokens", "output_tokens", "cache_write", "cache_read")
CODEX_CUMULATIVE_FIELDS = ("input_tokens", "output_tokens", "cached_input_tokens")


@dataclass(frozen=True)
class Usage:
    timestamp: datetime
    source: str
    project: str
    model: str
    input_tokens: int
    output_tokens: int
    cache_write: int
    cache_read: int

    @property
    def local_date(self) -> date:
        return self.timestamp.astimezone().date()


@dataclass
class ScanStats:
    malformed_lines: int = 0
    unreadable_files: int = 0


@dataclass(frozen=True)
class DateRange:
    since: Optional[date] = None
    until: Optional[date] = None

    def includes(self, value: date) -> bool:
        return not (
            (self.since is not None and value < self.since)
            or (self.until is not None and value > self.until)
        )

    @property
    def earliest_timestamp(self) -> Optional[float]:
        if self.since is None:
            return None
        local_midnight = datetime.combine(self.since, time.min).astimezone()
        return local_midnight.timestamp()


def parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            f"invalid date {value!r}; expected YYYY-MM-DD"
        ) from error


def parse_timestamp(value: object) -> Optional[datetime]:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def token_count(value: object) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        return 0
    return max(value, 0)


def project_name(value: object, fallback: str = "unknown") -> str:
    if not isinstance(value, str) or not value:
        return fallback
    name = Path(value.rstrip(os.sep)).name
    return name or value


def candidate_files(paths: Iterable[Path], date_range: DateRange) -> Iterator[Path]:
    """Skip files that cannot contain records at or after the requested start."""
    earliest = date_range.earliest_timestamp
    for path in sorted(paths):
        if earliest is not None:
            try:
                if path.stat().st_mtime < earliest:
                    continue
            except OSError:
                pass
        yield path


def read_json_lines(
    path: Path, stats: ScanStats, markers: Sequence[str] = ()
) -> Iterator[dict[str, object]]:
    try:
        with path.open(encoding="utf-8") as transcript:
            for line in transcript:
                if markers and not any(marker in line for marker in markers):
                    continue
                try:
                    record = json.loads(line)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    stats.malformed_lines += 1
                    continue
                if isinstance(record, dict):
                    yield record
    except OSError:
        stats.unreadable_files += 1


def claude_usage(
    root: Path, date_range: DateRange, stats: ScanStats
) -> Iterator[Usage]:
    """Yield last-seen usage for each Claude assistant request/message."""
    latest: dict[tuple[str, str], Usage] = {}
    paths = candidate_files(root.glob("*/*.jsonl"), date_range)

    for path in paths:
        fallback_project = path.parent.name
        records = read_json_lines(path, stats, ('"usage"',))
        for sequence, record in enumerate(records, 1):
            message = record.get("message")
            if not isinstance(message, dict) or message.get("role") != "assistant":
                continue
            usage = message.get("usage")
            if not isinstance(usage, dict):
                continue
            timestamp = parse_timestamp(record.get("timestamp"))
            if timestamp is None:
                continue

            request_id = record.get("requestId")
            message_id = message.get("id")
            if isinstance(request_id, str) and request_id:
                key = ("request", request_id)
            elif isinstance(message_id, str) and message_id:
                key = ("message", message_id)
            else:
                # Usage without either identifier cannot safely be deduplicated.
                key = ("record", f"{path}:{record.get('uuid', sequence)}")

            model = message.get("model")
            latest[key] = Usage(
                timestamp=timestamp,
                source="claude",
                project=project_name(record.get("cwd"), fallback_project),
                model=model if isinstance(model, str) and model else "unknown",
                input_tokens=token_count(usage.get("input_tokens")),
                output_tokens=token_count(usage.get("output_tokens")),
                cache_write=token_count(usage.get("cache_creation_input_tokens")),
                cache_read=token_count(usage.get("cache_read_input_tokens")),
            )

    yield from latest.values()


def cumulative_usage(value: object) -> Optional[dict[str, int]]:
    if not isinstance(value, dict):
        return None
    return {field: token_count(value.get(field)) for field in CODEX_CUMULATIVE_FIELDS}


def usage_delta(
    current: dict[str, int], previous: Optional[dict[str, int]]
) -> dict[str, int]:
    if previous is None or any(current[field] < previous[field] for field in current):
        return current.copy()
    return {field: current[field] - previous[field] for field in current}


def codex_usage(
    root: Path, date_range: DateRange, stats: ScanStats
) -> Iterator[Usage]:
    """Yield usage deltas from Codex's cumulative token_count events."""
    paths = candidate_files(root.rglob("*.jsonl"), date_range)

    for path in paths:
        project = "unknown"
        model = "unknown"
        previous: Optional[dict[str, int]] = None

        records = read_json_lines(
            path, stats, ('"session_meta"', '"turn_context"', '"token_count"')
        )
        for record in records:
            record_type = record.get("type")
            payload = record.get("payload")
            if not isinstance(payload, dict):
                continue

            if record_type == "session_meta":
                project = project_name(payload.get("cwd"), project)
                continue

            if record_type == "turn_context":
                project = project_name(payload.get("cwd"), project)
                context_model = payload.get("model")
                if isinstance(context_model, str) and context_model:
                    model = context_model
                continue

            if record_type != "event_msg" or payload.get("type") != "token_count":
                continue
            info = payload.get("info")
            if not isinstance(info, dict):
                continue
            current = cumulative_usage(info.get("total_token_usage"))
            if current is None:
                continue

            delta = usage_delta(current, previous)
            previous = current
            timestamp = parse_timestamp(record.get("timestamp"))
            if timestamp is None or not any(delta.values()):
                continue

            # Codex input_tokens includes cached_input_tokens. Split the two so
            # the displayed total counts cached input exactly once.
            cached = min(delta["cached_input_tokens"], delta["input_tokens"])
            yield Usage(
                timestamp=timestamp,
                source="codex",
                project=project,
                model=model,
                input_tokens=delta["input_tokens"] - cached,
                output_tokens=delta["output_tokens"],
                cache_write=0,
                cache_read=cached,
            )


def aggregate(
    records: Iterable[Usage],
    date_range: DateRange,
    by_project: bool,
    by_model: bool,
) -> tuple[list[str], list[list[object]]]:
    headers = ["date", "source"]
    if by_project:
        headers.append("project")
    if by_model:
        headers.append("model")
    headers.extend(["input", "output", "cache-write", "cache-read", "total"])

    totals: defaultdict[tuple[object, ...], list[int]] = defaultdict(
        lambda: [0] * len(TOKEN_FIELDS)
    )
    for record in records:
        local_date = record.local_date
        if not date_range.includes(local_date):
            continue
        key: tuple[object, ...] = (local_date.isoformat(), record.source)
        if by_project:
            key += (record.project,)
        if by_model:
            key += (record.model,)
        values = totals[key]
        for index, field in enumerate(TOKEN_FIELDS):
            values[index] += getattr(record, field)

    rows: list[list[object]] = []
    for key in sorted(totals):
        values = totals[key]
        rows.append([*key, *values, sum(values)])
    return headers, rows


def display_value(value: object) -> str:
    return f"{value:,}" if isinstance(value, int) else str(value)


def markdown_table(headers: Sequence[str], rows: Sequence[Sequence[object]]) -> str:
    numeric_start = len(headers) - 5

    def escape(value: object) -> str:
        return display_value(value).replace("\\", "\\\\").replace("|", "\\|")

    lines = ["| " + " | ".join(headers) + " |"]
    alignments = ["---" if index < numeric_start else "---:" for index in range(len(headers))]
    lines.append("| " + " | ".join(alignments) + " |")
    lines.extend("| " + " | ".join(escape(value) for value in row) + " |" for row in rows)
    return "\n".join(lines)


def plain_table(headers: Sequence[str], rows: Sequence[Sequence[object]]) -> str:
    rendered = [[display_value(value) for value in row] for row in rows]
    widths = [
        max(len(headers[index]), *(len(row[index]) for row in rendered))
        if rendered
        else len(headers[index])
        for index in range(len(headers))
    ]
    numeric_start = len(headers) - 5

    def format_row(row: Sequence[str]) -> str:
        cells = []
        for index, value in enumerate(row):
            aligned = (
                value.rjust(widths[index])
                if index >= numeric_start
                else value.ljust(widths[index])
            )
            cells.append(aligned)
        return "  ".join(cells)

    lines = [format_row(headers), "  ".join("-" * width for width in widths)]
    lines.extend(format_row(row) for row in rendered)
    return "\n".join(lines)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(
        description="Aggregate local Claude Code and Codex token usage by local date."
    )
    result.add_argument("--since", type=parse_date, help="include dates on or after YYYY-MM-DD")
    result.add_argument("--until", type=parse_date, help="include dates on or before YYYY-MM-DD")
    result.add_argument("--day", type=parse_date, help="include only YYYY-MM-DD")
    result.add_argument("--by-project", action="store_true", help="break totals down by project")
    result.add_argument("--by-model", action="store_true", help="break totals down by model")
    result.add_argument("--md", action="store_true", help="print a Markdown table")
    return result


def main(argv: Optional[Sequence[str]] = None) -> int:
    arguments = parser().parse_args(argv)
    if arguments.day is not None and (arguments.since is not None or arguments.until is not None):
        parser().error("--day cannot be combined with --since or --until")

    since = arguments.day or arguments.since
    until = arguments.day or arguments.until
    if since is not None and until is not None and since > until:
        parser().error("--since must be on or before --until")
    date_range = DateRange(since=since, until=until)

    home = Path.home()
    stats = ScanStats()
    records = list(claude_usage(home / ".claude" / "projects", date_range, stats))
    records.extend(codex_usage(home / ".codex" / "sessions", date_range, stats))
    headers, rows = aggregate(
        records,
        date_range,
        by_project=arguments.by_project,
        by_model=arguments.by_model,
    )
    print(markdown_table(headers, rows) if arguments.md else plain_table(headers, rows))

    if stats.malformed_lines or stats.unreadable_files:
        print(
            f"warning: skipped {stats.malformed_lines} malformed line(s) and "
            f"{stats.unreadable_files} unreadable file(s)",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
