from collections import defaultdict
from datetime import datetime
from models import valid_categories


def get_verified_date(prompt='Please enter date (YYYY-MM-DD): '):
    while True:
        date_str = input(prompt).strip()
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            print('Invalid date format. Please use YYYY-MM-DD (e.g. 2026-04-15).')


def get_verified_input():
    while True:
        try:
            amount = float(input('Please enter the amount: '))
            if amount <= 0:
                print('The amount must be greater than 0, please try again.')
                continue
            return amount
        except ValueError:
            print('Invalid input, please enter a number.')


def get_safe_category():
    print("Available categories:", ', '.join(valid_categories))
    while True:
        category = input("Enter category: ").strip()
        if category in valid_categories:
            return category
        print('Invalid category. Please choose from', valid_categories)


def filter_by_category(database, category):
    return [t for t in database if t['category'] == category]


def filter_by_date_range(database, start_date, end_date):
    return [t for t in database if start_date <= t['date'] <= end_date]


def generate_summary_statistics(database):
    if not database:
        print("\n[!] No data available to analyze.")
        return

    total_spending = 0
    category_totals = defaultdict(float)
    monthly_totals = defaultdict(float)

    for record in database:
        amt = record['amount']
        cat = record['category']
        total_spending += amt
        category_totals[cat] += amt
        monthly_totals[record['date'][:7]] += amt

    print("\n" + "=" * 40)
    print("      FINANCIAL SUMMARY REPORT      ")
    print("=" * 40)
    print(f"Total Transactions: {len(database)}")
    print(f"Total Spending    : HK${total_spending:.2f}")

    print("\n[ Category Breakdown ]")
    for cat, amt in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
        pct = (amt / total_spending) * 100
        print(f"  {cat:<13}: HK${amt:>8.2f}  ({pct:>5.1f}%)")

    print("\n[ Top 3 Categories ]")
    sorted_cats = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    for i, (cat, amt) in enumerate(sorted_cats[:3], 1):
        print(f"  {i}. {cat} — HK${amt:.2f}")

    print("\n[ Monthly Spending Trends ]")
    for month in sorted(monthly_totals):
        print(f"  {month}: HK${monthly_totals[month]:.2f}")

    try:
        parsed_dates = [datetime.strptime(t['date'], '%Y-%m-%d') for t in database]
        latest = max(parsed_dates)
        last7 = sum(t['amount'] for t in database if (latest - datetime.strptime(t['date'], '%Y-%m-%d')).days < 7)
        last30 = sum(t['amount'] for t in database if (latest - datetime.strptime(t['date'], '%Y-%m-%d')).days < 30)
        print("\n[ Recent Spending (relative to latest transaction) ]")
        print(f"  Last  7 days: HK${last7:.2f}")
        print(f"  Last 30 days: HK${last30:.2f}")
    except ValueError:
        pass

    print("=" * 40)
