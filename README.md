# comp1110
# Personal Budget & Spending Assistant

A command-line interface (CLI) Python application designed to help users track daily expenses, analyze spending habits, and set smart budget alerts. 

## Project Structure

* **`COMP1110-Budget-Assistant.py`**: The main entry point of the program, providing the complete interactive user menu.
* **`alerts.py`**: Handles budget warnings, including daily/weekly/monthly caps, percentage thresholds, uncategorized item checks, and consecutive overspending streaks.
* **`summary.py`**: The financial statistics module. It filters data, generates detailed spending trend reports (daily/weekly/monthly views), and manages user input verification.
* **`file_IO.py`**: The data persistence module that safely saves and loads transaction records and budget rules using JSON.
* **`test_data.py`**: A utility to generate random past-30-day transactions, edge cases, and uncategorized data for quick system testing.
* **`models.py`**: Defines the core data models, including valid expense categories (e.g., Food, Transport, Education) and functions for creating transactions and rules.

##  Key Features

### 1. Transaction Management
* **Record Expenses**: Add new transactions with specific dates, amounts, validated categories, and text descriptions.
* **Filter & Search**: View all records or narrow them down by specific categories or custom date ranges.

### 2. Data Storage
The application automatically creates and updates local JSON files in the root directory to persist your data between sessions safely:
* **text_transaction.json**: Stores your transaction history.
* **budget_rules.json**: Stores your active budget alert configurations.

### 3. In-Depth Financial Statistics
Automatically generate comprehensive financial reports:
* Total spending and transaction counts.
* Percentage breakdowns for all categories.
* Quick view of the top 3 highest-spending categories.
* Chronological spending trends (Daily, Weekly, and Monthly).
* Recent spending calculations (Last 7 days and Last 30 days).

### 4. Smart Budget Alerts
Configure custom rules to keep your finances in check. The system alerts you when:
* **Cap Limits**: A specific category exceeds a set monetary limit (Daily/Weekly/Monthly).
* **Percentage Limits**: A category takes up too much of your total spending ratio.
* **Overspending Streaks**: A daily cap is exceeded for 3 consecutive days.
* **Uncategorized Entries**: Transactions are logged as 'Others', prompting you to re-categorize them.

### 5. Built-in Testing & Case Studies
* **Case Studies**: Load pre-configured scenarios (Food Limit, Subscriptions, Transport) to see how the rules engine works.
* **Data Generator**: One-click generation of simulated transactions to easily test the application's reporting features.

##  Installation & Usage

1. Ensure you have **Python 3.x** installed on your machine.
2. Download all the `.py` files into a single folder.
3. Open your terminal or command prompt and navigate to the project directory.
4. Launch the application by running the following command:

   ```bash
   python COMP1110-Budget-Assistant.py
