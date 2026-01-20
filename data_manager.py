"""
Data management module for Personal Expense Tracker
Handles storage and retrieval of income and expense data
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd


class DataManager:
    """Manages data storage and retrieval for expenses and income"""
    
    def __init__(self, username: str = None, data_file: str = None):
        if data_file is None:
            if username:
                self.data_file = f"expense_data_{username}.json"
            else:
                self.data_file = "expense_data.json"
        else:
            self.data_file = data_file
        self.username = username
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load data from JSON file or create new structure"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._create_empty_data()
        return self._create_empty_data()
    
    def _create_empty_data(self) -> Dict:
        """Create empty data structure"""
        return {
            "income": [],
            "expenses": []
        }
    
    def _save_data(self):
        """Save data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add_income(self, amount: float, date: str, source: str = "", description: str = ""):
        """Add income entry"""
        income_entry = {
            "id": len(self.data["income"]) + 1,
            "amount": float(amount),
            "date": date,
            "source": source,
            "description": description,
            "timestamp": datetime.now().isoformat()
        }
        self.data["income"].append(income_entry)
        self._save_data()
        return income_entry
    
    def add_expense(self, amount: float, date: str, category: str, description: str = ""):
        """Add expense entry"""
        expense_entry = {
            "id": len(self.data["expenses"]) + 1,
            "amount": float(amount),
            "date": date,
            "category": category,
            "description": description,
            "timestamp": datetime.now().isoformat()
        }
        self.data["expenses"].append(expense_entry)
        self._save_data()
        return expense_entry
    
    def delete_income(self, income_id: int):
        """Delete income entry by ID"""
        self.data["income"] = [i for i in self.data["income"] if i["id"] != income_id]
        self._save_data()
    
    def delete_expense(self, expense_id: int):
        """Delete expense entry by ID"""
        self.data["expenses"] = [e for e in self.data["expenses"] if e["id"] != expense_id]
        self._save_data()
    
    def get_income_df(self) -> pd.DataFrame:
        """Get income data as pandas DataFrame"""
        if not self.data["income"]:
            return pd.DataFrame(columns=["id", "amount", "date", "source", "description", "timestamp"])
        df = pd.DataFrame(self.data["income"])
        df["date"] = pd.to_datetime(df["date"])
        return df
    
    def get_expenses_df(self) -> pd.DataFrame:
        """Get expenses data as pandas DataFrame"""
        if not self.data["expenses"]:
            return pd.DataFrame(columns=["id", "amount", "date", "category", "description", "timestamp"])
        df = pd.DataFrame(self.data["expenses"])
        df["date"] = pd.to_datetime(df["date"])
        return df
    
    def get_monthly_summary(self, year: int, month: int) -> Dict:
        """Get monthly summary for a specific year and month"""
        income_df = self.get_income_df()
        expenses_df = self.get_expenses_df()
        
        # Filter by month and year (only if DataFrames are not empty)
        if not income_df.empty:
            income_month = income_df[
                (income_df["date"].dt.year == year) & 
                (income_df["date"].dt.month == month)
            ]
        else:
            income_month = pd.DataFrame(columns=["id", "amount", "date", "source", "description", "timestamp"])
        
        if not expenses_df.empty:
            expenses_month = expenses_df[
                (expenses_df["date"].dt.year == year) & 
                (expenses_df["date"].dt.month == month)
            ]
        else:
            expenses_month = pd.DataFrame(columns=["id", "amount", "date", "category", "description", "timestamp"])
        
        total_income = income_month["amount"].sum() if not income_month.empty else 0
        total_expenses = expenses_month["amount"].sum() if not expenses_month.empty else 0
        net = total_income - total_expenses
        
        # Expenses by category
        expenses_by_category = expenses_month.groupby("category")["amount"].sum().to_dict() if not expenses_month.empty else {}
        
        return {
            "year": year,
            "month": month,
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net": net,
            "expenses_by_category": expenses_by_category,
            "income_df": income_month,
            "expenses_df": expenses_month
        }
    
    def get_yearly_summary(self, year: int) -> Dict:
        """Get yearly summary for a specific year"""
        income_df = self.get_income_df()
        expenses_df = self.get_expenses_df()
        
        # Filter by year (only if DataFrames are not empty)
        if not income_df.empty:
            income_year = income_df[income_df["date"].dt.year == year]
        else:
            income_year = pd.DataFrame(columns=["id", "amount", "date", "source", "description", "timestamp"])
        
        if not expenses_df.empty:
            expenses_year = expenses_df[expenses_df["date"].dt.year == year]
        else:
            expenses_year = pd.DataFrame(columns=["id", "amount", "date", "category", "description", "timestamp"])
        
        total_income = income_year["amount"].sum() if not income_year.empty else 0
        total_expenses = expenses_year["amount"].sum() if not expenses_year.empty else 0
        net = total_income - total_expenses
        
        # Monthly breakdown
        income_monthly = income_year.groupby(income_year["date"].dt.month)["amount"].sum().to_dict() if not income_year.empty else {}
        expenses_monthly = expenses_year.groupby(expenses_year["date"].dt.month)["amount"].sum().to_dict() if not expenses_year.empty else {}
        
        # Expenses by category
        expenses_by_category = expenses_year.groupby("category")["amount"].sum().to_dict() if not expenses_year.empty else {}
        
        return {
            "year": year,
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net": net,
            "expenses_by_category": expenses_by_category,
            "income_monthly": income_monthly,
            "expenses_monthly": expenses_monthly,
            "income_df": income_year,
            "expenses_df": expenses_year
        }
    
    def get_all_years(self) -> List[int]:
        """Get list of all years in the data"""
        income_df = self.get_income_df()
        expenses_df = self.get_expenses_df()
        
        all_dates = []
        if not income_df.empty:
            all_dates.extend(income_df["date"].dt.year.unique().tolist())
        if not expenses_df.empty:
            all_dates.extend(expenses_df["date"].dt.year.unique().tolist())
        
        return sorted(list(set(all_dates))) if all_dates else [datetime.now().year]
