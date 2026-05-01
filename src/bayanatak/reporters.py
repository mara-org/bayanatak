from __future__ import annotations

import csv
import io
import json
from typing import Any


def render(records: list[dict[str, Any]], output_format: str) -> str:
    if output_format == "json":
        return json.dumps(records, ensure_ascii=False, indent=2)
    if output_format == "csv":
        return render_csv(records)
    if output_format == "table":
        return render_table(records)
    raise ValueError(f"unsupported format: {output_format}")


def render_csv(records: list[dict[str, Any]]) -> str:
    if not records:
        return ""
    fields = sorted({key for record in records for key in record})
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    for record in records:
        writer.writerow({key: record.get(key, "") for key in fields})
    return output.getvalue().strip()


def render_table(records: list[dict[str, Any]]) -> str:
    if not records:
        return "لا توجد بيانات."
    fields = _visible_fields(records)
    rows = [[_cell(record.get(field, "")) for field in fields] for record in records]
    widths = [
        max(len(str(field)), *(len(row[index]) for row in rows))
        for index, field in enumerate(fields)
    ]
    header = "  ".join(str(field).ljust(widths[index]) for index, field in enumerate(fields))
    divider = "  ".join("-" * width for width in widths)
    body = [
        "  ".join(row[index].ljust(widths[index]) for index in range(len(fields)))
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def _visible_fields(records: list[dict[str, Any]]) -> list[str]:
    preferred = [
        "id",
        "order_id",
        "form_type",
        "name_ar",
        "customer",
        "full_name",
        "email",
        "phone",
        "mobile",
        "city",
        "item",
        "total_sar",
    ]
    keys = {key for record in records for key in record}
    fields = [field for field in preferred if field in keys]
    for key in sorted(keys):
        if key not in fields and len(fields) < 8:
            fields.append(key)
    return fields


def _cell(value: Any) -> str:
    if isinstance(value, bool):
        return "نعم" if value else "لا"
    return str(value)
