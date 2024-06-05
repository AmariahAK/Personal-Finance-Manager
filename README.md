# Personal Finance Manager

Welcome to the **Personal Finance Manager**! This CLI application helps you manage your finances effectively by tracking transactions, managing budgets, and generating financial reports. Whether you're looking to get a better handle on your spending or plan your savings, this tool is here to help.

## Features

### User Management
- **Add User**: Create a new user for the finance manager.
- **List Users**: Display all users.
- **Delete User**: Remove a user from the finance manager.

### Transaction Management
- **Add Transaction**: Record a new financial transaction.
- **List Transactions**: Display all transactions.
- **Search Transactions**: Find transactions based on amount, date, and category.
- **Delete Transaction**: Remove a specific transaction.

### Category Management
- **Add Category**: Create a new category for transactions.
- **List Categories**: Display all categories.

### Budget Management
- **Add Budget**: Set a budget for a specific category within a specified time period.
- **List Budgets**: Display all budgets.

### Recurring Transaction Management
- **Add Recurring Transaction**: Schedule a recurring transaction with a specified frequency.
- **List Recurring Transactions**: Display all recurring transactions.

### Reporting
- **Monthly Report**: Generate a report of transactions for a specific month.
- **Yearly Report**: Generate a report of transactions for a specific year.

## Installation

To install and set up the Personal Finance Manager, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/Personal-Finance-Manager
    ```

2. Create and activate a virtual environment using Pipenv:
    ```sh
    pip install pipenv
    pipenv install
    pipenv shell
    ```

3. Initialize the database:
    ```sh
    python -m finance_manager init
    ```

## Usage

After installation, you can use the CLI to manage your finances. Below are some example commands:

- **Initialize the database**:
    ```sh
    python -m finance_manager init
    ```

- **Add a user**:
    ```sh
    python -m finance_manager add-user --name "John Doe"
    ```

- **Add a category**:
    ```sh
    python -m finance_manager add-category --name "Groceries"
    ```

- **Add a transaction**:
    ```sh
    python -m finance_manager add-transaction --user_id 1 --category_id 1 --amount 50.75 --date 2024-06-01
    ```

- **Generate a monthly report**:
    ```sh
    python -m finance_manager monthly-report --user_id 1 --year 2024 --month 6
    ```

For a full list of commands and options, run:
```sh
python -m finance_manager --help

Contact
For any questions or support, please contact:

Amariah Kamau
📞 Phone: 0759336068
📧 Email: amariah.abish@gmail.com

Feel free to reach out if you have any feedback or need assistance!

Thank you for using the Personal Finance Manager. We hope it helps you achieve your financial goals! 🌟
