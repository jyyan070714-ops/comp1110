import random
from datetime import datetime, timedelta
from models import valid_categories, create_transaction

_descriptions = {
    'Food': ['Lunch at canteen', 'Dinner with friends', 'Grocery shopping', 'Coffee and snacks'],
    'Transport': ['MTR fare', 'Bus ride', 'Taxi home', 'Ferry ticket'],
    'Entertainment': ['Movie ticket', 'Streaming subscription', 'Concert ticket', 'Board game cafe'],
    'Shopping': ['Clothing', 'Electronics accessory', 'Books', 'Household items'],
    'Education': ['Textbook', 'Online course', 'Stationery', 'Printing fee'],
    'Sports': ['Gym monthly fee', 'Swimming pool', 'Sports equipment', 'Yoga class'],
    'Utilities': ['Phone bill', 'Internet bill', 'Electricity bill', 'Water bill'],
    'Health': ['Doctor visit', 'Pharmacy', 'Dentist', 'Vitamins'],
    'Others': ['Miscellaneous', 'Unknown expense'],
}


def generate_test_transactions(n=20, days_back=30, seed=None):
    if seed is not None:
        random.seed(seed)
    today = datetime.today()
    transactions = []
    for _ in range(n):
        date = (today - timedelta(days=random.randint(0, days_back))).strftime('%Y-%m-%d')
        category = random.choice(valid_categories)
        amount = round(random.uniform(5.0, 300.0), 1)
        description = random.choice(_descriptions[category])
        transactions.append(create_transaction(date, amount, category, description))
    return sorted(transactions, key=lambda t: t['date'])


def generate_edge_cases():
    today = datetime.today().strftime('%Y-%m-%d')
    old_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
    return [
        create_transaction(today, 0.1, 'Food', 'Minimum amount edge case'),
        create_transaction(today, 9999.9, 'Others', 'Large uncategorized expense'),
        create_transaction(old_date, 50.0, 'Transport', 'Old transaction from 1 year ago'),
        create_transaction(today, 100.0, 'Others', 'Second uncategorized expense'),
    ]
