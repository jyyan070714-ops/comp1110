from collections import defaultdict

valid_categories = ['Transport', 'Entertainment', 'Food', 'Shopping', 'Education', 'Sports', 'Utilities', 'Health', 'Others']

def get_verified_input():
    while True:
        a = input('Please enter the amount: ')
        try:
            amount = float(a)
            if amount <= 0:
                print('The amount must be bigger than 0, please try again: ')
                continue
            return amount # 修复了原代码缺少返回值的问题
        except ValueError:
            print('invalid input, please try again:')

def get_safe_category():
    print("Available categories: ", ', '.join(valid_categories))
    while True:
        category = input("Enter category: ")
        if category in valid_categories:
            return category
        print('Invalid category. Please choose from', valid_categories)

# ==========================================
# --- 你的任务：Summary Statistics 代码 ---
# ==========================================
def generate_summary_statistics(database):
    if not database:
        print("\n[!] No data available to analyze.")
        return

    total_spending = 0
    category_totals = defaultdict(float) # 用于按类别统计
    monthly_totals = defaultdict(float)  # 用于按月统计趋势

    for record in database:
        amt = record['amount']
        cat = record['category']
        date = record['date']
        
        # 1. 计算总额
        total_spending += amt
        
        # 2. 按类别累加
        category_totals[cat] += amt
        
        # 3. 按月份累加 (取 YYYY-MM)
        month = date[:7] 
        monthly_totals[month] += amt

    print("\n" + "="*40)
    print("      FINANCIAL SUMMARY REPORT      ")
    print("="*40)
    
    # 输出总支出
    print(f"Total Transactions: {len(database)}")
    print(f"Total Spending    : HK${total_spending:.2f}")

    # 输出各类别汇总
    print("\n[ Category Breakdown ]")
    for cat, amt in category_totals.items():
        percentage = (amt / total_spending) * 100
        print(f"- {cat:<13}: HK${amt:>8.2f} ({percentage:>5.1f}%)")

    # 输出前三名支出类别
    print("\n[ Top 3 Categories ]")
    sorted_cats = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    for i, (cat, amt) in enumerate(sorted_cats[:3], 1):
        print(f"{i}. {cat} (HK${amt:.2f})")

    # 输出时间趋势 (按月)
    print("\n[ Monthly Spending Trends ]")
    for month in sorted(monthly_totals.keys()):
        print(f"* {month}: HK${monthly_totals[month]:.2f}")
    
    print("="*40)

def main():
    temp_database = []
    while True:
        print("\n💰 This is Personal Budget & Spending Assistant 💰")
        print("1. Add a new transaction")
        print("2. View entered data (Test output)")
        print("3. View Summary Statistics (Your Task)") # 新增选项
        print("4. Exit system")
        
        choice = input("please select an option(1-4): ")
        if choice == '1':
            date = input('Please enter date (YYYY-MM-DD): ')
            amount = get_verified_input()
            category = get_safe_category()
            description = input('Please enter your description: ')
            new_transaction = {'date': date, 'amount': amount, 'category': category, 'description': description}
            temp_database.append(new_transaction)
            print("\nTransaction recorded!")
        elif choice == '2':
            if not temp_database:
                print("No transactions recorded yet.")
            else:
                for item in temp_database: print(item)
        elif choice == '3':
            # 执行你的统计任务
            generate_summary_statistics(temp_database)
        elif choice == '4':
            print("Exiting system!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()