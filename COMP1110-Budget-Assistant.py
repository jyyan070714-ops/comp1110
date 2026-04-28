import file_IO
import models
import summary
import alerts
import test_data

TRANSACTIONS_FILE = 'text_transaction.json'
RULES_FILE = 'budget_rules.json'
DEFAULT_TEST_TRANSACTIONS = 20


def _view_transactions(database):
    if not database:
        print("No transactions recorded yet.")
        return
    print("\n1. View all")
    print("2. Filter by category")
    print("3. Filter by date range")
    choice = input("Select (1-3): ").strip()

    if choice == '1':
        results = database
    elif choice == '2':
        category = summary.get_safe_category()
        results = summary.filter_by_category(database, category)
    elif choice == '3':
        start = summary.get_verified_date("Start date (YYYY-MM-DD): ")
        end = summary.get_verified_date("End date (YYYY-MM-DD): ")
        results = summary.filter_by_date_range(database, start, end)
    else:
        print("Invalid choice.")
        return

    if not results:
        print("No matching transactions.")
    else:
        print(f"\n{len(results)} transaction(s):")
        for t in results:
            print(f"  {t['date']} | {t['category']:<13} | HK${t['amount']:>8.2f} | {t['description']}")


def _get_percentage_threshold():
    while True:
        try:
            pct = float(input("Enter percentage threshold (e.g. 30 for 30%): "))
            if 0 < pct <= 100:
                return pct
            print("Must be between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 100.")


def _configure_budgets(rules):
    print("\n--- Budget Rules ---")
    print("1. Add rule")
    print("2. View all rules")
    print("3. Delete a rule")
    choice = input("Select (1-3): ").strip()

    if choice == '1':
        category = summary.get_safe_category()
        time_period = ''
        while time_period not in ('daily', 'weekly', 'monthly'):
            time_period = input("Time period (daily / weekly / monthly): ").strip().lower()
        alert_type = ''
        while alert_type not in ('cap', 'percentage'):
            alert_type = input("Alert type (cap / percentage): ").strip().lower()
        if alert_type == 'cap':
            threshold = summary.get_verified_input()
        else:
            threshold = _get_percentage_threshold()
        rules.append(models.create_budget_rule(category, time_period, threshold, alert_type))
        print("Rule added.")
    elif choice == '2':
        if not rules:
            print("No rules configured.")
        else:
            for i, r in enumerate(rules, 1):
                print(f"  {i}. {r['category']} | {r['time period']} | threshold: {r['threshold']} | type: {r['alert type']}")
    elif choice == '3':
        if not rules:
            print("No rules to delete.")
        else:
            for i, r in enumerate(rules, 1):
                print(f"  {i}. {r['category']} | {r['time period']} | threshold: {r['threshold']}")
            try:
                idx = int(input("Rule number to delete: ")) - 1
                if 0 <= idx < len(rules):
                    rules.pop(idx)
                    print("Rule deleted.")
                else:
                    print("Invalid number.")
            except ValueError:
                print("Invalid input.")

    return rules


CASE_STUDIES = {
    '1': ('Food Limit', 'case_food_limit.json'),
    '2': ('Subscriptions', 'case_subscriptions.json'),
    '3': ('Transport', 'case_transport.json'),
}


def _load_case_study():
    print("\n--- Load Case Study ---")
    for key, (name, _) in CASE_STUDIES.items():
        print(f"{key}. {name}")
    choice = input("Select (1-3): ").strip()
    if choice not in CASE_STUDIES:
        print("Invalid choice.")
        return None
    name, filepath = CASE_STUDIES[choice]
    data = file_IO.load_data(filepath)
    if data:
        print(f"Loaded {len(data)} transaction(s) from '{name}' case study.")
    return data


def _generate_test_data_menu(database):
    print("\n1. Random transactions (last 30 days)")
    print("2. Edge case transactions")
    print("3. All-uncategorized transactions")
    choice = input("Select (1-3): ").strip()

    if choice == '1':
        try:
            n = int(input(f"How many? (default {DEFAULT_TEST_TRANSACTIONS}): ").strip() or str(DEFAULT_TEST_TRANSACTIONS))
            if n <= 0:
                raise ValueError("Number of transactions must be positive")
        except ValueError:
            n = DEFAULT_TEST_TRANSACTIONS
        new_data = test_data.generate_test_transactions(n)
        database.extend(new_data)
        print(f"Generated {len(new_data)} test transactions.")
    elif choice == '2':
        edge = test_data.generate_edge_cases()
        database.extend(edge)
        print(f"Generated {len(edge)} edge case transactions.")
    elif choice == '3':
        uncategorized = test_data.generate_all_uncategorized()
        database.extend(uncategorized)
        print(f"Generated {len(uncategorized)} all-uncategorized transactions.")
    else:
        print("Invalid choice.")

    return database


def main():
    database = file_IO.load_data(TRANSACTIONS_FILE)
    rules = file_IO.load_rules(RULES_FILE)

    while True:
        print("\n💰 Personal Budget & Spending Assistant 💰")
        print("1. Add a new transaction")
        print("2. View transactions")
        print("3. Summary statistics")
        print("4. Check alerts")
        print("5. Configure budget rules")
        print("6. Generate test data")
        print("7. Load case study")
        print("8. Exit")
        choice = input("Select an option (1-8): ").strip()

        if choice == '1':
            date = summary.get_verified_date()
            amount = summary.get_verified_input()
            category = summary.get_safe_category()
            description = input('Description: ').strip()
            new_transaction = models.create_transaction(date, amount, category, description)
            database.append(new_transaction)
            file_IO.save_data(database, TRANSACTIONS_FILE)
            print("Transaction recorded!")
        elif choice == '2':
            _view_transactions(database)
        elif choice == '3':
            summary.generate_summary_statistics(database)
        elif choice == '4':
            alert_list = alerts.check_alerts(database, rules)
            if not alert_list:
                print("\nNo alerts. All spending within limits.")
            else:
                print(f"\n{len(alert_list)} alert(s):")
                for a in alert_list:
                    print(f"  {a}")
        elif choice == '5':
            rules = _configure_budgets(rules)
            file_IO.save_rules(rules, RULES_FILE)
        elif choice == '6':
            database = _generate_test_data_menu(database)
            file_IO.save_data(database, TRANSACTIONS_FILE)
        elif choice == '7':
            loaded = _load_case_study()
            if loaded is not None:
                database = loaded
                file_IO.save_data(database, TRANSACTIONS_FILE)
        elif choice == '8':
            file_IO.save_data(database, TRANSACTIONS_FILE)
            print("Exiting system!")
            break
        else:
            print("Invalid choice. Please enter 1-8.")


if __name__ == "__main__":
    main()
