"""Create tiny text-only synthetic manuals without third-party libraries."""

from __future__ import annotations

import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "day08_manuals"

MANUALS = {
    "ventilator-demo.pdf": [
        "DEMO MANUAL: VENTILATOR TRAINING ASSET",
        "This fictional document is for software retrieval practice only.",
        "It is not operating guidance and must never be used on a real device.",
        "Overview: the demo asset records a power state, alarm code and service note.",
        "Power indicator: record whether the external indicator is on or off.",
        "Alarm table (fictional training labels):",
        "Code V-01 | sensor warning | save the code and request authorized review.",
        "Code V-02 | battery notice | record the displayed notice for a technician.",
        "Code V-03 | maintenance reminder | add the reminder date to the demo log.",
        "Service record: include asset ID, timestamp, code and observed symptom.",
        "Safety boundary: only authorized personnel follow the real site's procedures.",
        "Support: route unresolved demo alerts to the training facilitator.",
    ],
    "infusion-pump-demo.pdf": [
        "DEMO MANUAL: INFUSION PUMP TRAINING ASSET",
        "This fictional document is for software retrieval practice only.",
        "It is not operating guidance and must never be used on a real device.",
        "Overview: the demo asset records a flow status, door sensor and service note.",
        "Status panel: copy the displayed text exactly into the demo ticket.",
        "Alarm table (fictional training labels):",
        "Code P-11 | flow notice | record the code; request authorized review.",
        "Code P-12 | door sensor notice | note the timestamp and asset ID.",
        "Code P-13 | self-check notice | preserve the message for a technician.",
        "Service record: include asset ID, timestamp, code and observed symptom.",
        "Safety boundary: do not change settings based on this training sample.",
        "Support: route unresolved demo alerts to the training facilitator.",
    ],
    "autoclave-demo.pdf": [
        "DEMO MANUAL: AUTOCLAVE TRAINING ASSET",
        "This fictional document is for software retrieval practice only.",
        "It is not operating guidance and must never be used on a real device.",
        "Overview: the demo asset records a cycle state, displayed temperature and alert.",
        "Display: record the visible value, timestamp and training asset ID.",
        "Alert table (fictional training labels):",
        "Code A-21 | temperature notice | record the value; request authorized review.",
        "Code A-22 | cycle notice | save the displayed message for a technician.",
        "Code A-23 | maintenance reminder | add the reminder date to the demo log.",
        "Service record: include asset ID, timestamp, code and observed symptom.",
        "Safety boundary: only authorized personnel follow the real site's procedures.",
        "Support: route unresolved demo alerts to the training facilitator.",
    ],
}


def escape_pdf(text: str) -> bytes:
    safe = text.encode("ascii", errors="replace").decode("ascii")
    return safe.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)").encode("ascii")


def write_pdf(path: Path, lines: list[str]) -> None:
    wrapped = [part for line in lines for part in textwrap.wrap(line, width=82) or [""]]
    commands = ["BT", "/F1 10 Tf", "48 790 Td", "14 TL"]
    commands += [f"({escape_pdf(line).decode('ascii')}) Tj T*" for line in wrapped]
    commands.append("ET")
    stream = "\n".join(commands).encode("ascii")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream",
    ]
    data = bytearray(b"%PDF-1.4\n% synthetic training file\n")
    offsets = [0]
    for number, obj in enumerate(objects, start=1):
        offsets.append(len(data))
        data.extend(f"{number} 0 obj\n".encode("ascii"))
        data.extend(obj + b"\nendobj\n")
    xref_offset = len(data)
    data.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    data.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        data.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    data.extend(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("ascii")
    )
    path.write_bytes(data)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, lines in MANUALS.items():
        write_pdf(OUT / name, lines)
    print(f"Created {len(MANUALS)} fictional manuals in {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
