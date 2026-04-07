valid_categories = ['Transport', 'Entertainment', 'Food', 'Shopping', 'Education', 'Sports', 'Utilities', 'Health', 'Others']

def get_verified_input():
    a=input('Please enter the amount: ')
    while True:
        try:
            amount=float(a)
            if amount<=0:
                print('The amount must be bigger than 0, please try again: ')
                continue
            break
        except ValueError:
            print('invalid input, please try again:')

def get_safe_category():
    print("Available categories: ",', '.join(valid_categories))
    while True:
        category = input("Enter category: ")
        if category in valid_categories:
            return category
        print('Invalid category. Please choose from',valid_categories)

def main():
    temp_database=[]
    while True:
        print("💰 This is Personal Budget & Spending Assistant 💰")
        print("1. Add a new transaction")
        print("2. View entered data (Test output)")
        print("3. Exit system")
        choice=input("please select an option(1-3): ")
        if choice=='1':
            date = input('Please enter date (YYYY-MM-DD): ')
            amount = get_verified_input()
            category = get_safe_category()
            description = input('Please enter your description: ')
            new_transaction = {'date': date,'amount': amount,'category': category,'description': description}
            temp_database.append(new_transaction)
            print("\nTransaction has been successfully validated and recorded!!!")
        elif choice=='2':
            if not temp_database:
                print("No transactions recorded yet.")
            else:
                for item in temp_database:
                    print(item)
        elif choice == '3':
            print("Data processing complete. Exiting system!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
