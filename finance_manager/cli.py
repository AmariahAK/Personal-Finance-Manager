import click
from sqlalchemy.orm import Session
from .database import SessionLocal, init_db
from .models import User, Transaction, Category, Budget, RecurringTransaction
from datetime import datetime

@click.group()
def cli():
    pass

@click.command()
def init():
    init_db()
    click.echo('Database initialized!')

@click.command()
@click.option('--name', prompt='User name', help='The name of the user.')
def add_user(name):
    session = SessionLocal()
    user = User(name=name)
    session.add(user)
    session.commit()
    session.close()
    click.echo(f'User {name} added!')

@click.command()
@click.option('--user_id', prompt='User ID', type=int, help='The ID of the user.')
@click.option('--amount', prompt='Amount', type=float, help='Transaction amount.')
@click.option('--category', prompt='Category', help='Category of the transaction.')
@click.option('--date', prompt='Date (YYYY-MM-DD)', help='Transaction date.')
def add_transaction(user_id, amount, category, date):
    session = SessionLocal()
    category_obj = session.query(Category).filter_by(name=category).first()
    if not category_obj:
        category_obj = Category(name=category)
        session.add(category_obj)
        session.commit()

    transaction_date = datetime.strptime(date, "%Y-%m-%d").date()
    transaction = Transaction(user_id=user_id, amount=amount, category_id=category_obj.id, date=transaction_date)
    session.add(transaction)
    session.commit()
    session.close()
    click.echo('Transaction added!')

@click.command()
@click.option('--name', prompt='Category name', help='The name of the category.')
def add_category(name):
    session = SessionLocal()
    category = Category(name=name)
    session.add(category)
    session.commit()
    session.close()
    click.echo(f'Category {name} added!')

@click.command()
def list_users():
    session = SessionLocal()
    users = session.query(User).all()
    for user in users:
        click.echo(f'ID: {user.id}, Name: {user.name}')
    session.close()

@click.command()
@click.option('--user_id', prompt='User ID', type=int, help='The ID of the user.')
def list_transactions(user_id):
    session = SessionLocal()
    transactions = session.query(Transaction).filter_by(user_id=user_id).all()
    for transaction in transactions:
        click.echo(f'ID: {transaction.id}, Amount: {transaction.amount}, Date: {transaction.date}, Category: {transaction.category.name}')
    session.close()

@click.command()
def list_categories():
    session = SessionLocal()
    categories = session.query(Category).all()
    for category in categories:
        click.echo(f'ID: {category.id}, Name: {category.name}')
    session.close()

@click.command()
@click.option('--category', prompt='Category name', help='The name of the category.')
def list_transactions_by_category(category):
    session = SessionLocal()
    category_obj = session.query(Category).filter_by(name=category).first()
    if not category_obj:
        click.echo(f'Category {category} not found.')
        return
    transactions = session.query(Transaction).filter_by(category_id=category_obj.id).all()
    for transaction in transactions:
        click.echo(f'ID: {transaction.id}, Amount: {transaction.amount}, Date: {transaction.date}, User: {transaction.user.name}')
    session.close()

@click.command()
@click.option('--user_id', prompt='User ID', type=int, help='The ID of the user.')
@click.option('--month', prompt='Month (MM)', type=int, help='The month for the report.')
@click.option('--year', prompt='Year (YYYY)', type=int, help='The year for the report.')
def monthly_report(user_id, month, year):
    session = SessionLocal()
    transactions = session.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.date.between(f"{year}-{month}-01", f"{year}-{month}-31")
    ).all()
    income = sum(t.amount for t in transactions if t.amount > 0)
    expenses = sum(t.amount for t in transactions if t.amount < 0)
    click.echo(f"Income for {month}/{year}: {income}")
    click.echo(f"Expenses for {month}/{year}: {expenses}")
    click.echo(f"Savings for {month}/{year}: {income + expenses}")
    session.close()

@click.command()
@click.option('--user_id', prompt='User ID', type=int, help='The ID of the user.')
@click.option('--year', prompt='Year (YYYY)', type=int, help='The year for the report.')
def yearly_report(user_id, year):
    session = SessionLocal()
    transactions = session.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.date.between(f"{year}-01-01", f"{year}-12-31")
    ).all()
    income = sum(t.amount for t in transactions if t.amount > 0)
    expenses = sum(t.amount for t in transactions if t.amount < 0)
    click.echo(f"Income for {year}: {income}")
    click.echo(f"Expenses for {year}: {expenses}")
    click.echo(f"Savings for {year}: {income + expenses}")
    session.close()

@click.command()
@click.option('--user_id', prompt='User ID', type=int, help='The ID of the user.')
@click.option('--category', prompt='Category', help='The name of the category.')
@click.option('--amount', prompt='Amount', type=float, help='Budget amount.')
@click.option('--start_date', prompt='Start Date (YYYY-MM-DD)', help='Budget start date.')
@click.option('--end_date', prompt='End Date (YYYY-MM-DD)', help='Budget end date.')
def add_budget(user_id, category, amount, start_date, end_date):
    session = SessionLocal()
    category_obj = session.query(Category).filter_by(name=category).first()
    if not category_obj:
        category_obj = Category(name=category)
        session.add(category_obj)
        session.commit()

    budget = Budget(user_id=user_id, category_id=category_obj.id, amount=amount,
                    start_date=datetime.strptime(start_date, "%Y-%m-%d").date(),
                    end_date=datetime.strptime(end_date, "%Y-%m-%d").date())
    session.add(budget)
    session.commit()
    session.close()
    click.echo('Budget added!')

@click.command()
@click.option('--user_id', prompt='User ID', type=int, help='The ID of the user.')
def list_budgets(user_id):
    session = SessionLocal()
    budgets = session.query(Budget).filter_by(user_id=user_id).all()
    for budget in budgets:
        click.echo(f'ID: {budget.id}, Category: {budget.category.name}, Amount: {budget.amount}, '
                   f'Start Date: {budget.start_date}, End Date: {budget.end_date}')
    session.close()

@click.command()
@click.option('--user_id', prompt='User ID', type=int, help='The ID of the user.')
@click.option('--amount', prompt='Amount', type=float, help='Transaction amount.')
@click.option('--category', prompt='Category', help='Category of the transaction.')
@click.option('--start_date', prompt='Start Date (YYYY-MM-DD)', help='Start date of the recurring transaction.')
@click.option('--frequency', prompt='Frequency (daily, weekly, monthly, yearly)', help='Frequency of the transaction.')
def add_recurring_transaction(user_id, amount, category, start_date, frequency):
    session = SessionLocal()
    category_obj = session.query(Category).filter_by(name=category).first()
    if not category_obj:
        category_obj = Category(name=category)
        session.add(category_obj)
        session.commit()

    recurring_transaction = RecurringTransaction(user_id=user_id, amount=amount, category_id=category_obj.id,
                                                 start_date=datetime.strptime(start_date, "%Y-%m-%d").date(),
                                                 frequency=frequency)
    session.add(recurring_transaction)
    session.commit()
    session.close()
    click.echo('Recurring transaction added!')

@click.command()
@click.option('--user_id', prompt='User ID', type=int, help='The ID of the user.')
def list_recurring_transactions(user_id):
    session = SessionLocal()
    recurring_transactions = session.query(RecurringTransaction).filter_by(user_id=user_id).all()
    for rt in recurring_transactions:
        click.echo(f'ID: {rt.id}, Category: {rt.category.name}, Amount: {rt.amount}, '
                   f'Start Date: {rt.start_date}, Frequency: {rt.frequency}')
    session.close()

@click.command()
@click.option('--user_id', prompt='User ID', type=int, help='The ID of the user.')
@click.option('--start_date', prompt='Start Date (YYYY-MM-DD)', help='Start date of the transactions.')
@click.option('--end_date', prompt='End Date (YYYY-MM-DD)', help='End date of the transactions.')
@click.option('--min_amount', prompt='Minimum Amount', type=float, default=None, help='Minimum amount of the transactions.')
@click.option('--max_amount', prompt='Maximum Amount', type=float, default=None, help='Maximum amount of the transactions.')
@click.option('--category', prompt='Category', default=None, help='Category of the transactions.')
def search_transactions(user_id, start_date, end_date, min_amount, max_amount, category):
    session = SessionLocal()
    query = session.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.date.between(start_date, end_date)
    )

    if min_amount is not None:
        query = query.filter(Transaction.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(Transaction.amount <= max_amount)
    if category:
        category_obj = session.query(Category).filter_by(name=category).first()
        if category_obj:
            query = query.filter(Transaction.category_id == category_obj.id)

    transactions = query.all()
    for transaction in transactions:
        click.echo(f'ID: {transaction.id}, Amount: {transaction.amount}, Date: {transaction.date}, Category: {transaction.category.name}')
    session.close()

@click.command()
@click.option('--user_id', prompt='User ID', type=int, help='The ID of the user.')
def delete_user(user_id):
    session = SessionLocal()
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        session.delete(user)
        session.commit()
        click.echo(f'User {user_id} deleted!')
    else:
        click.echo(f'User {user_id} not found.')
    session.close()

@click.command()
@click.option('--transaction_id', prompt='Transaction ID', type=int, help='The ID of the transaction.')
def delete_transaction(transaction_id):
    session = SessionLocal()
    transaction = session.query(Transaction).filter_by(id=transaction_id).first()
    if transaction:
        session.delete(transaction)
        session.commit()
        click.echo(f'Transaction {transaction_id} deleted!')
    else:
        click.echo(f'Transaction {transaction_id} not found.')
    session.close()

cli.add_command(init)
cli.add_command(add_user)
cli.add_command(add_transaction)
cli.add_command(add_category)
cli.add_command(list_users)
cli.add_command(list_transactions)
cli.add_command(list_categories)
cli.add_command(list_transactions_by_category)
cli.add_command(monthly_report)
cli.add_command(yearly_report)
cli.add_command(add_budget)
cli.add_command(list_budgets)
cli.add_command(add_recurring_transaction)
cli.add_command(list_recurring_transactions)
cli.add_command(search_transactions)
cli.add_command(delete_user)
cli.add_command(delete_transaction)

if __name__ == '__main__':
    cli()
