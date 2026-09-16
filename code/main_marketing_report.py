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

if len(sys.argv) > 1:
    try:
        seed = int(sys.argv[1])
    except ValueError:
        print("Seed must be an integer.")
        sys.exit(1)
else:
    seed = None

from sales_pipeline import (
    get_raw_sales_data,
    clean_sales_data,
    summarize_by_item,
    find_top_entry,

)

# --- The report ------------------------------------------------------------------
#
# 
print("=== MARKETING: Revenue by Item ===")
print()  # blank line

# --- Step 1: Extract ---------------------------------------------

raw_data = get_raw_sales_data(seed)
clean_data = clean_sales_data(raw_data)
item_summary = summarize_by_item(clean_data)
top_by_revenue = find_top_entry(item_summary, field="revenue")
top_by_units = find_top_entry(item_summary, field="units_sold")

# --- Step 3: Load -----------------------------------------------

# Print the item table, one line per item, with totals formatted with commas and 2 decimals

print(f"{'Item':<20} {'Units Sold':>12} {'Revenue':>12}")
for entry in item_summary:
    print(f"{entry['item']:<20} {entry['units_sold']:>12} ${entry['revenue']:>11,.2f}")

print()  # blank line

# Print the top sellers exactly with spacing aligned

print(f"Top seller by revenue: {top_by_revenue['item']} (${top_by_revenue['revenue']:,.2f})")
print(f"Top seller by units:   {top_by_units['item']} ({top_by_units['units_sold']} units)")