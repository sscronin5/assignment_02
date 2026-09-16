"""
transform.py — the **T** in ETL.

Transform is where messy input becomes numbers you can do arithmetic on. Every
function in here takes values in and returns a value out: no `input()`, no
`print()`, no files. That is what makes them easy to unit test and easy to reuse
from *any* report.

The one rule that matters: **never crash on bad data.** A single row with a price
of `"N/A"` must not take down a report covering hundreds of good rows. When a value
cannot be read, coerce it to zero and keep going.

Your job: implement the seven functions below so the Unit Tests in
tests/test_unit.py all pass. Each docstring says exactly what the function should
return, gives worked examples, and ends with a **How to build it** section — read
that before you start typing. Replace the `# TODO` line (and the `pass`) with your
code.

Write them in the order the README's build order table gives. Nothing later needs
anything you have not written yet.
"""


def clean_currency(value) -> float:
    if value is None:
        return 0.0
    try:
        return float(str(value).replace("$", "").replace(",", "").strip())
    except ValueError:
        return 0.0



def clean_quantity(value) -> int:
    if value is None:
        return 0
    try:
        return int(str(value).strip())
    except ValueError:
        return 0




def clean_sales_data(raw_data: list[dict]) -> list[dict]:
    cleaned_rows = []
    for row in raw_data:
        cleaned_row = {
            "date": row["date"],
            "item": row["item"],
            "price": clean_currency(row["price"]),
            "qty": clean_quantity(row["qty"]),
        }
        cleaned_row["total_revenue"] = cleaned_row["price"] * cleaned_row["qty"]
        cleaned_rows.append(cleaned_row)
    return cleaned_rows



def calculate_total_revenue(cleaned_data: list[dict]) -> float:
    total = 0.0
    for row in cleaned_data:
        total += row["total_revenue"]
    return total


def summarize_by_item(cleaned_data: list[dict]) -> list[dict]:
    totals = {}
    for row in cleaned_data:
        item = row["item"]
        if item not in totals:
            totals[item] = {"item": item, "units_sold": 0, "revenue": 0.0}
        totals[item]["units_sold"] += row["qty"]
        totals[item]["revenue"] += row["total_revenue"]

    sorted_totals = sorted(
        totals.values(),
        key=lambda entry: (-entry['revenue'], entry['item'])
    )

    return sorted_totals

def summarize_by_day(cleaned_data: list[dict]) -> list[dict]:
  totals = {}

  for row in cleaned_data:
    date = row["date"]
    if date not in totals:
      totals[date] = {"date": date, "units_sold": 0, "revenue": 0.0}
    totals[date]["units_sold"] += row.get("qty", 0)
    totals[date]["revenue"] += row.get("total_revenue", 0.0)


  sorted_totals = sorted(totals.values(), key=lambda entry: entry['date'])
  return sorted_totals


def find_top_entry(summary: list[dict], field: str = "revenue") -> dict:
    if not summary:
        return {}

    top = summary[0]
    for entry in summary[1:]:
        if entry[field] > top[field]:
            top = entry

    return top
