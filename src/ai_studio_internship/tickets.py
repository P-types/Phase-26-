"""Validate synthetic service-ticket CSV files with Pydantic."""

from __future__ import annotations

import argparse
import csv
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Literal, Sequence

from pydantic import BaseModel, ConfigDict, Field, ValidationError

logger = logging.getLogger(__name__)


class ServiceTicket(BaseModel):
    """A validated service ticket from the synthetic AMC dataset."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    ticket_id: str = Field(min_length=1, max_length=32, pattern=r"^[A-Z0-9][A-Z0-9_-]*$")
    hospital: str = Field(min_length=1, max_length=120)
    equipment: str = Field(min_length=1, max_length=80)
    description: str = Field(min_length=1, max_length=1000)
    urgency: Literal["low", "medium", "high", "critical"]
    created_at: datetime


@dataclass(frozen=True)
class TicketIssue:
    """A row-level issue; input values are omitted from diagnostics."""

    row_number: int
    messages: tuple[str, ...]


@dataclass
class TicketImportResult:
    """Validated tickets and safe diagnostics for rejected rows."""

    rows_seen: int
    tickets: list[ServiceTicket]
    issues: list[TicketIssue]


def _validation_messages(error: ValidationError) -> tuple[str, ...]:
    messages: list[str] = []
    for detail in error.errors():
        location = ".".join(str(part) for part in detail["loc"]) or "row"
        messages.append(f"{location}: {detail['msg']}")
    return tuple(messages)


def load_tickets_csv(path: str | Path) -> TicketImportResult:
    """Read, validate, and de-duplicate ticket rows from a CSV file.

    The first CSV record is the header, so row-level diagnostics start at 2.
    Invalid rows are reported without echoing their contents, which keeps
    logs safer if the loader is reused later.
    """

    csv_path = Path(path)
    tickets: list[ServiceTicket] = []
    issues: list[TicketIssue] = []
    seen_ticket_ids: set[str] = set()
    rows_seen = 0

    with csv_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None:
            raise ValueError("CSV file must include a header row")

        required_fields = set(ServiceTicket.model_fields)
        missing_fields = sorted(required_fields - set(reader.fieldnames))
        if missing_fields:
            missing = ", ".join(missing_fields)
            raise ValueError(f"CSV is missing required columns: {missing}")

        for row_number, row in enumerate(reader, start=2):
            rows_seen += 1
            try:
                ticket = ServiceTicket.model_validate(row)
            except ValidationError as error:
                messages = _validation_messages(error)
                issues.append(TicketIssue(row_number, messages))
                logger.warning("Rejected CSV row %d: %s", row_number, "; ".join(messages))
                continue

            if ticket.ticket_id in seen_ticket_ids:
                message = "ticket_id: duplicate ticket ID in CSV"
                issues.append(TicketIssue(row_number, (message,)))
                logger.warning("Rejected CSV row %d: %s", row_number, message)
                continue

            seen_ticket_ids.add(ticket.ticket_id)
            tickets.append(ticket)

    return TicketImportResult(rows_seen=rows_seen, tickets=tickets, issues=issues)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the ticket CSV validator as a command-line program."""

    parser = argparse.ArgumentParser(description="Validate an AMC service-ticket CSV")
    parser.add_argument("csv_path", type=Path, help="path to the ticket CSV")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    try:
        result = load_tickets_csv(args.csv_path)
    except (OSError, ValueError) as error:
        parser.exit(status=2, message=f"error: {error}\n")

    logger.info("Rows read: %d", result.rows_seen)
    logger.info("Valid tickets: %d", len(result.tickets))
    logger.info("Invalid rows: %d", len(result.issues))

    return 1 if result.issues else 0
