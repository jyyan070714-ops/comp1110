valid_categories = [
    'Transport',
    'Entertainment',
    'Food',
    'Shopping',
    'Education',
    'Sports',
    'Utilities',
    'Health',
    'Others'
]

def create_transaction(date, amount, category, description, optional_notes=''):
    
    if category not in valid_categories:
        print(f"Warning: Category '{category}' is not in the system's default list!"))

    transaction = {
        'date': date,
        'amount': float(amount),
        'category': category,
        'description': description,
        'optional notes': optional_notes
    }
    
    return transaction

def create_budget_rule(category, time_period, threshold, alert_type):
    rule = {
        'category': category,
        'time period': time_period,
        'threshold': threshold,
        'alert type': alert_type
    }

    return rule

