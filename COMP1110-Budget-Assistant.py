import file_IO
import models
import summary

def main():
    filename = 'text_transaction.json'
    temp_database = file_IO.load_data(filename)

    while True:
        print("\n💰 This is Personal Budget & Spending Assistant 💰")
        print("1. Add a new transaction")
        print("2. View entered data")
        print("3. View Summary Statistics")
        print("4. Exit system")
        choice = input("please select an option(1-4): ")
        
        if choice == '1':
            date = input('Please enter date (YYYY-MM-DD): ')
            amount = summary.get_verified_input() 
            category = summary.get_safe_category()
            description = input('Please enter your description: ')
            
            new_transaction = models.create_transaction(date, amount, category, description)
            temp_database.append(new_transaction)
            
            file_IO.save_data(temp_database, filename)
            print("\nTransaction has been successfully validated and recorded!!!")
            
        elif choice == '2':
            if not temp_database:
                print("No transactions recorded yet.")
            else:
                for item in temp_database:
                    print(item)
                    
        elif choice == '3':
            summary.generate_summary_statistics(temp_database)
            
        elif choice == '4':
            file_IO.save_data(temp_database, filename)
            print("Data processing complete. Exiting system!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
