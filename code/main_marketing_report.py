"""
main_marketing_report.py — the Marketing department's report.

Marketing does not care about individual transactions. They care about *products*:
which one earns the most money, and which one moves the most units. Those are
frequently not the same product, and the gap between them is the interesting part.

This is the payoff for building a package instead of a script. Marketing needs a
roll-up that Finance never asked for, so `summarize_by_item` and `find_top_entry`
were **added** to `sales_pipeline.transform` — and `main_finance_report.py` did
not change by a single character. That is what modular means: the package grows
by addition, not by editing everyone who already depends on it.

Before running:  pip install -r requirements.txt

    python code/main_marketing_report.py        # the fixed sample data
    python code/main_marketing_report.py 42     # the generated data for seed 42
"""

import sys

from sales_pipeline import (
    clean_sales_data,
    find_top_entry,
    get_raw_sales_data,
    print_item_table,
    summarize_by_item,
)

# --- Reading the dataset seed ----------------------------------------------------
# A missing or blank argument means "use the sample data".

seed = None
if len(sys.argv) > 1 and sys.argv[1].strip() != "":
    seed = int(sys.argv[1])


# --- The report ------------------------------------------------------------------

print("=== MARKETING: Revenue by Item ===")
print()

# Extract
raw_data = get_raw_sales_data(seed)

# Transform
clean_data = clean_sales_data(raw_data)
item_summary = summarize_by_item(clean_data)
top_by_revenue = find_top_entry(item_summary, "revenue")
top_by_units = find_top_entry(item_summary, "units_sold")

# Load
print_item_table(item_summary)
print()

print(f"Top seller by revenue: {top_by_revenue['item']} (${top_by_revenue['revenue']:,.2f})")
print(f"Top seller by units:   {top_by_units['item']} ({top_by_units['units_sold']} units)")