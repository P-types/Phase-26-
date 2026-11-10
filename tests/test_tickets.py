import csv
from pathlib import Path

import pytest
from pydantic import ValidationError

from ai_studio_internship.tickets import ServiceTicket, load_tickets_csv


def valid_row(**changes: str) -> dict[str, str]:
    row = {
        "ticket_id": "AMC-2026-001",
        "hospital": "Demo Hospital North",
        "equipment": "Ventilator",
        "description": "Alarm panel shows a recurring sensor warning",
        "urgency": "high",
        "created_at": "2026-10-12T09:15:00+05:30",
    }
    row.update(changes)
    return row


def write_csv(
    path: Path,
    rows: list[dict[str, str]],
    headers: list[str] | None = None,
) -> None:
    columns = headers or list(valid_row())
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def test_valid_ticket_is_parsed_and_strings_are_trimmed() -> None:
    ticket = ServiceTicket.model_validate(valid_row(ticket_id=" AMC-2026-001 "))

    assert ticket.ticket_id == "AMC-2026-001"
    assert ticket.urgency == "high"
    assert ticket.created_at.isoformat() == "2026-10-12T09:15:00+05:30"


def test_invalid_urgency_is_rejected() -> None:
    with pytest.raises(ValidationError):
        ServiceTicket.model_validate(valid_row(urgency="emergency"))


def test_loader_separates_valid_and_invalid_rows(tmp_path: Path) -> None:
    csv_path = tmp_path / "tickets.csv"
    write_csv(
        csv_path,
        [
            valid_row(),
            valid_row(ticket_id="AMC-2026-002", hospital=""),
            valid_row(ticket_id="AMC-2026-003", urgency="urgent"),
        ],
    )

    result = load_tickets_csv(csv_path)

    assert result.rows_seen == 3
    assert len(result.tickets) == 1
    assert [issue.row_number for issue in result.issues] == [3, 4]
    assert "hospital" in result.issues[0].messages[0]


def test_duplicate_ticket_id_is_reported(tmp_path: Path) -> None:
    csv_path = tmp_path / "tickets.csv"
    write_csv(csv_path, [valid_row(), valid_row(description="A second synthetic issue")])

    result = load_tickets_csv(csv_path)

    assert len(result.tickets) == 1
    assert result.issues[0].row_number == 3
    assert "duplicate ticket ID" in result.issues[0].messages[0]


def test_missing_required_column_is_reported(tmp_path: Path) -> None:
    csv_path = tmp_path / "tickets.csv"
    write_csv(csv_path, [], headers=["ticket_id", "hospital"])

    with pytest.raises(ValueError, match="missing required columns"):
        load_tickets_csv(csv_path)


def test_invalid_datetime_is_rejected() -> None:
    with pytest.raises(ValidationError):
        ServiceTicket.model_validate(valid_row(created_at="not-a-date"))
