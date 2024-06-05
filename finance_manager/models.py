from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)

    transactions = relationship("Transaction", back_populates="user")
    budgets = relationship("Budget", back_populates="user")
    recurring_transactions = relationship("RecurringTransaction", back_populates="user")

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)

    transactions = relationship("Transaction", back_populates="category")
    budgets = relationship("Budget", back_populates="category")
    recurring_transactions = relationship("RecurringTransaction", back_populates="category")

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)

    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")

class Budget(Base):
    __tablename__ = 'budgets'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    amount = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    user = relationship("User", back_populates="budgets")
    category = relationship("Category", back_populates="budgets")

class RecurringTransaction(Base):
    __tablename__ = 'recurring_transactions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    amount = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    frequency = Column(String, nullable=False)  # 'daily', 'weekly', 'monthly', 'yearly'

    user = relationship("User", back_populates="recurring_transactions")
    category = relationship("Category", back_populates="recurring_transactions")
