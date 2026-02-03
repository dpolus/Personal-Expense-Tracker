"""
Personal Expense Tracker Application
A comprehensive tool for tracking income and expenses with visualizations
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import os
from data_manager import DataManager
from auth_manager import AuthManager
from financial_health import FinancialHealthAnalyzer

# Page configuration
st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Remove top white space
st.markdown("""
    <style>
    .main .block-container {
        padding-top: 0rem;
        padding-bottom: 2rem;
    }
    .stApp > header {
        background-color: transparent;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'username' not in st.session_state:
    st.session_state.username = None

if 'auth_manager' not in st.session_state:
    st.session_state.auth_manager = AuthManager()

if 'data_manager' not in st.session_state:
    st.session_state.data_manager = None

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Add Income/Expense"

if 'show_register' not in st.session_state:
    st.session_state.show_register = False

# Common expense categories
EXPENSE_CATEGORIES = [
    "Food & Dining",
    "Transportation",
    "Shopping",
    "Bills & Utilities",
    "Entertainment",
    "Healthcare",
    "Education",
    "Travel",
    "Personal Care",
    "Gifts & Donations",
    "Housing",
    "Other"
]

def format_currency(amount):
    """Format amount as currency"""
    return f"${amount:,.2f}"

def create_nav_bar():
    """Create a top navigation bar with improved styling"""
    # Add custom CSS for better navigation bar
    st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        border-radius: 0.5rem;
        font-weight: 500;
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    nav_options = {
        "➕ Add Transaction": "Add Income/Expense",
        "📅 Monthly Summary": "Monthly Summary",
        "📊 Yearly Summary": "Yearly Summary",
        "💚 Financial Health": "Financial Health",
        "📋 All Transactions": "All Transactions",
        "👤 Profile": "Profile",
        "⚙️ Settings": "Settings"
    }
    
    # Create navigation bar with buttons in a container
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    cols = st.columns(len(nav_options), gap="small")
    
    for idx, (label, page_name) in enumerate(nav_options.items()):
        with cols[idx]:
            # Highlight current page
            is_active = st.session_state.current_page == page_name
            button_type = "primary" if is_active else "secondary"
            
            if st.button(label, key=f"nav_{page_name}", use_container_width=True, type=button_type):
                st.session_state.current_page = page_name
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_login_page():
    """Display login and registration page"""
    st.title("💰 Personal Expense Tracker")
    st.markdown("")
    
    # Show registration form or login form based on state
    if st.session_state.show_register:
        show_registration_form()
    else:
        show_login_form()

def show_login_form():
    """Display login form"""
    st.markdown("### 🔐 Login to Your Account")
    st.markdown("")
    
    with st.form("login_form"):
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        login_submitted = st.form_submit_button("Login", use_container_width=True)
        
        if login_submitted:
            if username and password:
                auth_manager = st.session_state.auth_manager
                success, message = auth_manager.authenticate_user(username, password)
                
                if success:
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.session_state.data_manager = DataManager(username=username)
                    st.success(f"Welcome back, {username}!")
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please enter both username and password")
    
    st.markdown("")
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Don't have an account? Register here", use_container_width=True, key="show_register_btn"):
            st.session_state.show_register = True
            st.rerun()

def show_registration_form():
    """Display registration form"""
    st.markdown("### 📝 Create New Account")
    st.markdown("")
    
    with st.form("register_form"):
        new_username = st.text_input("Username", key="reg_username")
        new_password = st.text_input("Password", type="password", key="reg_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password")
        email = st.text_input("Email (optional)", key="reg_email")
        full_name = st.text_input("Full Name (optional)", key="reg_full_name")
        register_submitted = st.form_submit_button("Register", use_container_width=True)
        
        if register_submitted:
            if not new_username or not new_password:
                st.error("Username and password are required")
            elif new_password != confirm_password:
                st.error("Passwords do not match")
            else:
                auth_manager = st.session_state.auth_manager
                success, message = auth_manager.register_user(new_username, new_password, email, full_name)
                
                if success:
                    st.success(message + " Please log in now.")
                    st.session_state.show_register = False
                    st.rerun()
                else:
                    st.error(message)
    
    st.markdown("")
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Already have an account? Login here", use_container_width=True, key="show_login_btn"):
            st.session_state.show_register = False
            st.rerun()

def main():
    # Check authentication
    if not st.session_state.authenticated:
        show_login_page()
        return
    
    # User is authenticated - show main app
    username = st.session_state.username
    
    # Title with user info and logout
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("💰 Personal Expense Tracker")
    with col2:
        st.markdown("")
        st.markdown("")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.session_state.data_manager = None
            st.session_state.current_page = "Add Income/Expense"
            # Clear financial health data to prevent data leakage between users
            if 'health_score_data' in st.session_state:
                del st.session_state.health_score_data
            st.rerun()
    
    st.markdown(f"**Logged in as:** {username}")
    st.markdown("")
    
    # Navigation bar
    create_nav_bar()
    st.markdown("")
    
    data_manager = st.session_state.data_manager
    
    if data_manager is None:
        st.error("Data manager not initialized. Please log out and log back in.")
        return
    
    page = st.session_state.current_page
    
    if page == "Add Income/Expense":
        show_add_transactions(data_manager)
    elif page == "Monthly Summary":
        show_monthly_summary(data_manager)
    elif page == "Yearly Summary":
        show_yearly_summary(data_manager)
    elif page == "Financial Health":
        show_financial_health(data_manager)
    elif page == "All Transactions":
        show_all_transactions(data_manager)
    elif page == "Profile":
        show_profile(data_manager)
    elif page == "Settings":
        show_settings(data_manager)

def show_add_transactions(data_manager):
    """Display form to add income and expenses"""
    st.markdown("### 💸 Add Income or Expense")
    st.markdown("Enter your income and expenses to track your finances")
    st.markdown("")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("#### ➕ Add Income")
        st.markdown("")
        with st.form("income_form", clear_on_submit=True):
            income_amount = st.number_input("Amount ($)", min_value=0.01, step=0.01, key="income_amount")
            income_date = st.date_input("Date", value=date.today(), key="income_date")
            income_source = st.text_input("Source (e.g., Salary, Freelance)", key="income_source")
            income_description = st.text_area("Description (optional)", key="income_desc")
            
            income_submitted = st.form_submit_button("Add Income", use_container_width=True)
            
            if income_submitted:
                if income_amount > 0:
                    data_manager.add_income(
                        income_amount,
                        income_date.strftime("%Y-%m-%d"),
                        income_source,
                        income_description
                    )
                    st.success(f"✅ Income of {format_currency(income_amount)} added successfully!")
                else:
                    st.error("Please enter a valid amount.")
    
    with col2:
        st.markdown("#### ➖ Add Expense")
        st.markdown("")
        with st.form("expense_form", clear_on_submit=True):
            expense_amount = st.number_input("Amount ($)", min_value=0.01, step=0.01, key="expense_amount")
            expense_date = st.date_input("Date", value=date.today(), key="expense_date")
            expense_category = st.selectbox("Category", EXPENSE_CATEGORIES, key="expense_category")
            expense_description = st.text_area("Description (optional)", key="expense_desc")
            
            expense_submitted = st.form_submit_button("Add Expense", use_container_width=True)
            
            if expense_submitted:
                if expense_amount > 0:
                    data_manager.add_expense(
                        expense_amount,
                        expense_date.strftime("%Y-%m-%d"),
                        expense_category,
                        expense_description
                    )
                    st.success(f"✅ Expense of {format_currency(expense_amount)} added successfully!")
                else:
                    st.error("Please enter a valid amount.")
    
    # Quick stats
    st.markdown("---")
    st.markdown("### 📊 Quick Overview")
    show_quick_stats(data_manager)

def show_quick_stats(data_manager):
    """Display quick statistics"""
    income_df = data_manager.get_income_df()
    expenses_df = data_manager.get_expenses_df()
    
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Current month stats
    month_summary = data_manager.get_monthly_summary(current_year, current_month)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Monthly Income", format_currency(month_summary["total_income"]))
    with col2:
        st.metric("Monthly Expenses", format_currency(month_summary["total_expenses"]))
    with col3:
        st.metric("Monthly Net", format_currency(month_summary["net"]), 
                 delta=format_currency(month_summary["net"]) if month_summary["net"] >= 0 else None)
    with col4:
        total_transactions = len(income_df) + len(expenses_df)
        st.metric("Total Transactions", total_transactions)

def show_monthly_summary(data_manager):
    """Display monthly summary with visualizations"""
    st.markdown("### 📅 Monthly Summary")
    st.markdown("View detailed breakdown of your income and expenses for a specific month")
    st.markdown("")
    
    # Get available years
    available_years = data_manager.get_all_years()
    
    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox("Select Year", available_years, index=len(available_years)-1)
    with col2:
        selected_month = st.selectbox("Select Month", 
                                      list(range(1, 13)), 
                                      index=datetime.now().month - 1,
                                      format_func=lambda x: datetime(1900, x, 1).strftime("%B"))
    
    month_summary = data_manager.get_monthly_summary(selected_year, selected_month)
    
    # Summary cards
    st.markdown("#### Summary Statistics")
    st.markdown("")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Income", format_currency(month_summary["total_income"]))
    with col2:
        st.metric("Total Expenses", format_currency(month_summary["total_expenses"]))
    with col3:
        st.metric("Net Amount", format_currency(month_summary["net"]),
                 delta=format_currency(month_summary["net"]) if month_summary["net"] >= 0 else None)
    with col4:
        savings_rate = ((month_summary["total_income"] - month_summary["total_expenses"]) / month_summary["total_income"] * 100) if month_summary["total_income"] > 0 else 0
        st.metric("Savings Rate", f"{savings_rate:.1f}%")
    
    st.markdown("---")
    
    # Visualizations
    if month_summary["expenses_by_category"]:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Expenses by Category (Pie Chart)")
            categories = list(month_summary["expenses_by_category"].keys())
            amounts = list(month_summary["expenses_by_category"].values())
            
            fig_pie = px.pie(
                values=amounts,
                names=categories,
                title="Expense Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.subheader("Expenses by Category (Bar Chart)")
            fig_bar = px.bar(
                x=categories,
                y=amounts,
                title="Expenses by Category",
                labels={"x": "Category", "y": "Amount ($)"},
                color=amounts,
                color_continuous_scale="Reds"
            )
            fig_bar.update_layout(showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # Detailed tables
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Income Details")
        if not month_summary["income_df"].empty:
            income_display = month_summary["income_df"][["date", "amount", "source", "description"]].copy()
            income_display["amount"] = income_display["amount"].apply(format_currency)
            income_display["date"] = income_display["date"].dt.strftime("%Y-%m-%d")
            st.dataframe(income_display, use_container_width=True, hide_index=True)
        else:
            st.info("No income recorded for this month.")
    
    with col2:
        st.subheader("Expense Details")
        if not month_summary["expenses_df"].empty:
            expenses_display = month_summary["expenses_df"][["date", "amount", "category", "description"]].copy()
            expenses_display["amount"] = expenses_display["amount"].apply(format_currency)
            expenses_display["date"] = expenses_display["date"].dt.strftime("%Y-%m-%d")
            st.dataframe(expenses_display, use_container_width=True, hide_index=True)
        else:
            st.info("No expenses recorded for this month.")

def show_yearly_summary(data_manager):
    """Display yearly summary with visualizations"""
    st.markdown("### 📊 Yearly Summary")
    st.markdown("Comprehensive annual analysis of your financial trends and patterns")
    st.markdown("")
    
    # Get available years
    available_years = data_manager.get_all_years()
    selected_year = st.selectbox("Select Year", available_years, index=len(available_years)-1)
    
    year_summary = data_manager.get_yearly_summary(selected_year)
    
    # Summary cards
    st.markdown("#### Summary Statistics")
    st.markdown("")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Income", format_currency(year_summary["total_income"]))
    with col2:
        st.metric("Total Expenses", format_currency(year_summary["total_expenses"]))
    with col3:
        st.metric("Net Amount", format_currency(year_summary["net"]),
                 delta=format_currency(year_summary["net"]) if year_summary["net"] >= 0 else None)
    with col4:
        avg_monthly = year_summary["total_expenses"] / 12 if year_summary["total_expenses"] > 0 else 0
        st.metric("Avg Monthly Expenses", format_currency(avg_monthly))
    
    st.markdown("---")
    
    # Monthly trends
    if year_summary["income_monthly"] or year_summary["expenses_monthly"]:
        st.subheader("Monthly Trends")
        
        months = list(range(1, 13))
        month_names = [datetime(1900, m, 1).strftime("%B") for m in months]
        income_values = [year_summary["income_monthly"].get(m, 0) for m in months]
        expense_values = [year_summary["expenses_monthly"].get(m, 0) for m in months]
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=month_names,
            y=income_values,
            mode='lines+markers',
            name='Income',
            line=dict(color='green', width=3),
            marker=dict(size=8)
        ))
        fig_trend.add_trace(go.Scatter(
            x=month_names,
            y=expense_values,
            mode='lines+markers',
            name='Expenses',
            line=dict(color='red', width=3),
            marker=dict(size=8)
        ))
        fig_trend.update_layout(
            title="Income vs Expenses Over the Year",
            xaxis_title="Month",
            yaxis_title="Amount ($)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        if year_summary["expenses_by_category"]:
            st.subheader("Yearly Expenses by Category")
            categories = list(year_summary["expenses_by_category"].keys())
            amounts = list(year_summary["expenses_by_category"].values())
            
            fig_pie = px.pie(
                values=amounts,
                names=categories,
                title="Yearly Expense Distribution",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        if year_summary["expenses_by_category"]:
            st.subheader("Top Expense Categories")
            categories = list(year_summary["expenses_by_category"].keys())
            amounts = list(year_summary["expenses_by_category"].values())
            
            # Sort by amount
            sorted_data = sorted(zip(categories, amounts), key=lambda x: x[1], reverse=True)
            top_categories = [x[0] for x in sorted_data[:10]]
            top_amounts = [x[1] for x in sorted_data[:10]]
            
            fig_bar = px.bar(
                x=top_amounts,
                y=top_categories,
                orientation='h',
                title="Top Expense Categories",
                labels={"x": "Amount ($)", "y": "Category"},
                color=top_amounts,
                color_continuous_scale="Reds"
            )
            fig_bar.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # Monthly comparison bar chart
    if year_summary["income_monthly"] or year_summary["expenses_monthly"]:
        st.markdown("---")
        st.subheader("Monthly Income vs Expenses Comparison")
        
        months = list(range(1, 13))
        month_names = [datetime(1900, m, 1).strftime("%B") for m in months]
        income_values = [year_summary["income_monthly"].get(m, 0) for m in months]
        expense_values = [year_summary["expenses_monthly"].get(m, 0) for m in months]
        
        fig_comparison = go.Figure()
        fig_comparison.add_trace(go.Bar(
            name='Income',
            x=month_names,
            y=income_values,
            marker_color='green'
        ))
        fig_comparison.add_trace(go.Bar(
            name='Expenses',
            x=month_names,
            y=expense_values,
            marker_color='red'
        ))
        fig_comparison.update_layout(
            title="Monthly Income vs Expenses",
            xaxis_title="Month",
            yaxis_title="Amount ($)",
            barmode='group',
            height=400
        )
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Summary table
    st.markdown("---")
    st.subheader("Yearly Summary Table")
    
    summary_data = {
        "Metric": ["Total Income", "Total Expenses", "Net Amount", "Average Monthly Income", "Average Monthly Expenses"],
        "Amount": [
            format_currency(year_summary["total_income"]),
            format_currency(year_summary["total_expenses"]),
            format_currency(year_summary["net"]),
            format_currency(year_summary["total_income"] / 12 if year_summary["total_income"] > 0 else 0),
            format_currency(year_summary["total_expenses"] / 12 if year_summary["total_expenses"] > 0 else 0)
        ]
    }
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

def show_all_transactions(data_manager):
    """Display all transactions with ability to delete"""
    st.markdown("### 📋 All Transactions")
    st.markdown("View and manage all your income and expense entries")
    st.markdown("")
    
    income_df = data_manager.get_income_df()
    expenses_df = data_manager.get_expenses_df()
    
    tab1, tab2 = st.tabs(["Income", "Expenses"])
    
    with tab1:
        st.subheader("Income Transactions")
        if not income_df.empty:
            income_display = income_df[["id", "date", "amount", "source", "description"]].copy()
            income_display["amount"] = income_display["amount"].apply(format_currency)
            income_display["date"] = income_display["date"].dt.strftime("%Y-%m-%d")
            st.dataframe(income_display, use_container_width=True, hide_index=True)
            
            # Delete option
            st.markdown("### Delete Income Entry")
            income_ids = income_df["id"].tolist()
            delete_income_id = st.selectbox("Select Income ID to Delete", income_ids, key="delete_income")
            if st.button("Delete Income Entry", key="btn_delete_income"):
                data_manager.delete_income(delete_income_id)
                st.success("Income entry deleted!")
                st.rerun()
        else:
            st.info("No income transactions recorded.")
    
    with tab2:
        st.subheader("Expense Transactions")
        if not expenses_df.empty:
            expenses_display = expenses_df[["id", "date", "amount", "category", "description"]].copy()
            expenses_display["amount"] = expenses_display["amount"].apply(format_currency)
            expenses_display["date"] = expenses_display["date"].dt.strftime("%Y-%m-%d")
            st.dataframe(expenses_display, use_container_width=True, hide_index=True)
            
            # Delete option
            st.markdown("### Delete Expense Entry")
            expense_ids = expenses_df["id"].tolist()
            delete_expense_id = st.selectbox("Select Expense ID to Delete", expense_ids, key="delete_expense")
            if st.button("Delete Expense Entry", key="btn_delete_expense"):
                data_manager.delete_expense(delete_expense_id)
                st.success("Expense entry deleted!")
                st.rerun()
        else:
            st.info("No expense transactions recorded.")

def show_profile(data_manager):
    """Display and edit user profile"""
    st.markdown("### 👤 User Profile")
    st.markdown("Manage your account information and preferences")
    st.markdown("")
    
    username = st.session_state.username
    auth_manager = st.session_state.auth_manager
    user = auth_manager.get_user(username)
    
    if user:
        # Display current profile information
        st.markdown("#### Account Information")
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Username", value=user.get("username", ""), disabled=True)
            email_key = "profile_email"
            full_name_key = "profile_full_name"
            if email_key not in st.session_state:
                st.session_state[email_key] = user.get("email", "")
            if full_name_key not in st.session_state:
                st.session_state[full_name_key] = user.get("full_name", "")
            st.text_input("Email", value=st.session_state[email_key], key=email_key)
            st.text_input("Full Name", value=st.session_state[full_name_key], key=full_name_key)
        
        with col2:
            created_at = user.get("created_at", "")
            if created_at:
                try:
                    created_date = datetime.fromisoformat(created_at).strftime("%Y-%m-%d %H:%M")
                    st.text_input("Account Created", value=created_date, disabled=True)
                except:
                    st.text_input("Account Created", value=created_at, disabled=True)
            
            last_login = user.get("last_login", "")
            if last_login:
                try:
                    login_date = datetime.fromisoformat(last_login).strftime("%Y-%m-%d %H:%M")
                    st.text_input("Last Login", value=login_date, disabled=True)
                except:
                    st.text_input("Last Login", value=last_login, disabled=True)
        
        # Update profile button
        if st.button("Update Profile", use_container_width=True):
            email = st.session_state.get("profile_email", user.get("email", ""))
            full_name = st.session_state.get("profile_full_name", user.get("full_name", ""))
            auth_manager.update_user_profile(username, email=email, full_name=full_name)
            st.success("Profile updated successfully!")
            st.rerun()
        
        st.markdown("---")
        
        # Change password section
        st.markdown("#### Change Password")
        st.markdown("")
        with st.form("change_password_form", clear_on_submit=False):
            old_password = st.text_input("Current Password", type="password", key="old_pass")
            new_password = st.text_input("New Password", type="password", key="new_pass")
            confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_pass")
            st.markdown("")
            change_pass_submitted = st.form_submit_button("🔒 Update Password", use_container_width=True, type="primary")
            
            if change_pass_submitted:
                if not old_password or not new_password:
                    st.error("Please fill in all password fields")
                elif new_password != confirm_password:
                    st.error("New passwords do not match")
                else:
                    success, message = auth_manager.change_password(username, old_password, new_password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        
        st.markdown("---")
        
        # Profile preferences
        st.markdown("#### Preferences")
        profile_prefs = user.get("profile", {})
        
        col1, col2, col3 = st.columns(3)
        with col1:
            currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "JPY", "CAD", "AUD"], 
                                   index=["USD", "EUR", "GBP", "JPY", "CAD", "AUD"].index(profile_prefs.get("currency", "USD")) if profile_prefs.get("currency", "USD") in ["USD", "EUR", "GBP", "JPY", "CAD", "AUD"] else 0,
                                   key="profile_currency")
        with col2:
            date_format = st.selectbox("Date Format", ["YYYY-MM-DD", "MM/DD/YYYY", "DD/MM/YYYY"],
                                     index=["YYYY-MM-DD", "MM/DD/YYYY", "DD/MM/YYYY"].index(profile_prefs.get("date_format", "YYYY-MM-DD")) if profile_prefs.get("date_format", "YYYY-MM-DD") in ["YYYY-MM-DD", "MM/DD/YYYY", "DD/MM/YYYY"] else 0,
                                     key="profile_date_format")
        with col3:
            theme = st.selectbox("Theme", ["light", "dark"],
                               index=["light", "dark"].index(profile_prefs.get("theme", "light")) if profile_prefs.get("theme", "light") in ["light", "dark"] else 0,
                               key="profile_theme")
        
        if st.button("Save Preferences", use_container_width=True):
            auth_manager.update_user_profile(username, currency=currency, date_format=date_format, theme=theme)
            st.success("Preferences saved successfully!")
            st.rerun()

def show_settings(data_manager):
    """Display settings and data management options"""
    st.markdown("### ⚙️ Settings")
    st.markdown("Manage your data and application settings")
    st.markdown("")
    
    st.subheader("Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Export Data")
        if st.button("Export to CSV", use_container_width=True):
            income_df = data_manager.get_income_df()
            expenses_df = data_manager.get_expenses_df()
            
            if not income_df.empty or not expenses_df.empty:
                # Create a combined export
                export_data = []
                for _, row in income_df.iterrows():
                    export_data.append({
                        "Type": "Income",
                        "Date": row["date"].strftime("%Y-%m-%d"),
                        "Amount": row["amount"],
                        "Category/Source": row.get("source", ""),
                        "Description": row.get("description", "")
                    })
                for _, row in expenses_df.iterrows():
                    export_data.append({
                        "Type": "Expense",
                        "Date": row["date"].strftime("%Y-%m-%d"),
                        "Amount": -row["amount"],
                        "Category/Source": row.get("category", ""),
                        "Description": row.get("description", "")
                    })
                
                export_df = pd.DataFrame(export_data)
                csv = export_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"expense_tracker_export_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No data to export.")
    
    with col2:
        st.markdown("### Data Statistics")
        income_df = data_manager.get_income_df()
        expenses_df = data_manager.get_expenses_df()
        
        st.metric("Total Income Entries", len(income_df))
        st.metric("Total Expense Entries", len(expenses_df))
        st.metric("Total Transactions", len(income_df) + len(expenses_df))
    
    st.markdown("---")
    st.subheader("About")
    st.info("""
    **Personal Expense Tracker** v1.0
    
    Track your income and expenses with comprehensive monthly and yearly summaries.
    Features include:
    - Income and expense tracking
    - Monthly and yearly summaries
    - Multiple visualization formats (charts, tables)
    - Data export functionality
    
    Data is stored locally in user-specific files (`expense_data_<username>.json`).
    """)

def show_financial_health(data_manager):
    """Display Financial Health Score with AI-powered analysis"""
    st.markdown("### 💚 Financial Health Score")
    st.markdown("AI-powered analysis of your financial situation with personalized recommendations")
    st.markdown("")
    
    # Check if API key is set
    api_key = None
    # Try to get from Streamlit secrets (if available)
    # Note: Accessing st.secrets will trigger file loading, so we catch any errors
    try:
        api_key = st.secrets.get("TOGETHER_API_KEY", None)
    except (FileNotFoundError, AttributeError, KeyError, Exception):
        # Secrets file doesn't exist, key not found, or any other error - that's okay
        # We'll fall back to environment variable
        pass
    
    # Fallback to environment variable
    if not api_key:
        api_key = os.getenv("TOGETHER_API_KEY", None)
    
    if not api_key:
        st.warning("⚠️ **Together.ai API Key Required**")
        st.info("""
        To use the Financial Health Score feature, you need to set your Together.ai API key.
        
        **Option 1: Environment Variable (Recommended)**
        ```bash
        # Windows PowerShell
        $env:TOGETHER_API_KEY="your-api-key-here"
        
        # Windows CMD
        set TOGETHER_API_KEY=your-api-key-here
        
        # macOS/Linux
        export TOGETHER_API_KEY=your-api-key-here
        ```
        
        **Option 2: Streamlit Secrets**
        Create a `.streamlit/secrets.toml` file with:
        ```toml
        TOGETHER_API_KEY = "your-api-key-here"
        ```
        
        Get your API key from: https://api.together.xyz/
        """)
        
        # Show fallback metrics without AI
        st.markdown("---")
        st.subheader("📊 Basic Financial Metrics")
        show_basic_metrics(data_manager)
        return
    
    # Model selection - Using serverless models that don't require dedicated endpoints
    st.markdown("#### ⚙️ AI Model Settings")
    available_models = [
        "meta-llama/Llama-2-7b-chat-hf",  # Serverless - good for free tier
        "meta-llama/Llama-2-70b-chat-hf",  # Serverless
        "mistralai/Mistral-7B-Instruct-v0.1",  # Serverless
        "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO",  # Serverless
        "meta-llama/Llama-3-70b-chat-hf",  # May require dedicated endpoint
        "mistralai/Mixtral-8x7B-Instruct-v0.1",  # May require dedicated endpoint
    ]
    
    selected_model = st.selectbox(
        "Select AI Model (Serverless models recommended)",
        available_models,
        index=0,
        help="Start with 'meta-llama/Llama-2-7b-chat-hf' for free tier. If you get a 400 error about 'non-serverless model', try a different serverless model."
    )
    
    # Initialize analyzer with selected model
    analyzer = FinancialHealthAnalyzer(api_key=api_key)
    analyzer.model = selected_model
    
    # Button to generate/refresh score
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.info(f"💡 Click the button below to generate your AI-powered financial health analysis using {selected_model}")
    with col2:
        if st.button("🔄 Refresh Analysis", use_container_width=True):
            if 'health_score_data' in st.session_state:
                del st.session_state.health_score_data
    
    # Generate or retrieve health score
    if 'health_score_data' not in st.session_state:
        with st.spinner("🤖 Analyzing your financial data with AI... This may take a few seconds."):
            try:
                health_data = analyzer.generate_health_score(data_manager)
                st.session_state.health_score_data = health_data
            except Exception as e:
                error_msg = str(e)
                st.error(f"❌ Error generating health score: {error_msg}")
                
                # Provide troubleshooting help
                if "400" in error_msg or "Bad Request" in error_msg:
                    if "non-serverless" in error_msg.lower() or "dedicated endpoint" in error_msg.lower():
                        st.warning("""
                        **400 Error: Model Requires Dedicated Endpoint**
                        
                        The selected model requires a dedicated endpoint and isn't available as serverless.
                        
                        **Solution:**
                        1. **Select a serverless model** - Try "meta-llama/Llama-2-7b-chat-hf" (recommended for free tier)
                        2. **Or create a dedicated endpoint** - Visit the model page to set up a dedicated endpoint
                        3. **Check available serverless models** - Visit https://together.ai/models and filter for serverless models
                        
                        The app will use fallback calculations instead.
                        """)
                    else:
                        st.warning("""
                        **400 Bad Request Error - Troubleshooting:**
                        
                        1. **Try a different model** - The selected model might not be available on your Together.ai plan
                        2. **Check your API key** - Verify your API key is valid at https://api.together.xyz/
                        3. **Check model availability** - Visit https://together.ai/models to see available models
                        4. **API credits** - Ensure you have sufficient credits in your Together.ai account
                        
                        The app will use fallback calculations instead.
                        """)
                elif "401" in error_msg or "Unauthorized" in error_msg:
                    st.warning("""
                    **401 Unauthorized Error:**
                    
                    Your API key might be invalid or expired. Please:
                    1. Check your API key at https://api.together.xyz/
                    2. Regenerate your API key if needed
                    3. Make sure the key is set correctly in your environment variable
                    """)
                elif "429" in error_msg or "rate limit" in error_msg.lower():
                    st.warning("""
                    **Rate Limit Error:**
                    
                    You've exceeded the API rate limit. Please wait a moment and try again.
                    """)
                
                st.info("Showing basic metrics instead.")
                show_basic_metrics(data_manager)
                return
    else:
        health_data = st.session_state.health_score_data
    
    # Display Health Score
    st.markdown("---")
    score = health_data.get("score", 70)
    
    # Score visualization
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Determine score color
        if score >= 80:
            score_color = "🟢"
            score_label = "Excellent"
            score_color_hex = "#28a745"
        elif score >= 60:
            score_color = "🟡"
            score_label = "Good"
            score_color_hex = "#ffc107"
        elif score >= 40:
            score_color = "🟠"
            score_label = "Fair"
            score_color_hex = "#fd7e14"
        else:
            score_color = "🔴"
            score_label = "Needs Improvement"
            score_color_hex = "#dc3545"
        
        # Display score with visual
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, {score_color_hex}15 0%, {score_color_hex}05 100%); border-radius: 1rem; border: 2px solid {score_color_hex}40;">
            <h1 style="font-size: 4rem; margin: 0; color: {score_color_hex};">{score}</h1>
            <h3 style="margin: 0.5rem 0; color: {score_color_hex};">{score_color} {score_label}</h3>
            <p style="color: #666; margin: 0;">Financial Health Score</p>
        </div>
        """, unsafe_allow_html=True)
        
        if "score_explanation" in health_data:
            st.markdown(f"*{health_data['score_explanation']}*")
    
    st.markdown("")
    
    # Analysis Section
    if "analysis" in health_data:
        st.markdown("### 📝 Financial Analysis")
        st.markdown(health_data["analysis"])
        st.markdown("")
    
    # Strengths and Concerns
    col1, col2 = st.columns(2)
    
    with col1:
        if "strengths" in health_data and health_data["strengths"]:
            st.markdown("### ✅ Strengths")
            strengths = health_data["strengths"]
            # Handle both list and single string cases
            if isinstance(strengths, list):
                for strength in strengths:
                    # Handle both string and dict cases
                    if isinstance(strength, str):
                        st.markdown(f"• {strength}")
                    elif isinstance(strength, dict):
                        st.markdown(f"• {strength.get('text', strength.get('description', str(strength)))}")
                    else:
                        st.markdown(f"• {str(strength)}")
            elif isinstance(strengths, str):
                st.markdown(f"• {strengths}")
            else:
                st.markdown(f"• {str(strengths)}")
    
    with col2:
        if "concerns" in health_data and health_data["concerns"]:
            st.markdown("### ⚠️ Areas for Improvement")
            concerns = health_data["concerns"]
            # Handle both list and single string cases
            if isinstance(concerns, list):
                for concern in concerns:
                    # Handle both string and dict cases
                    if isinstance(concern, str):
                        st.markdown(f"• {concern}")
                    elif isinstance(concern, dict):
                        st.markdown(f"• {concern.get('text', concern.get('description', str(concern)))}")
                    else:
                        st.markdown(f"• {str(concern)}")
            elif isinstance(concerns, str):
                st.markdown(f"• {concerns}")
            else:
                st.markdown(f"• {str(concerns)}")
    
    st.markdown("---")
    
    # Recommendations
    if "recommendations" in health_data and health_data["recommendations"]:
        st.markdown("### 💡 Personalized Recommendations")
        
        recommendations = health_data["recommendations"]
        
        # Handle different recommendation formats
        if isinstance(recommendations, str):
            # Single string recommendation
            with st.expander("🟡 **Recommendation** (Priority: Medium)"):
                st.markdown(recommendations)
        elif isinstance(recommendations, list):
            # List of recommendations
            for idx, rec in enumerate(recommendations, 1):
                if isinstance(rec, dict):
                    # Expected format: dict with priority, title, description
                    priority = rec.get("priority", "medium")
                    if isinstance(priority, str):
                        priority = priority.lower()
                    else:
                        priority = "medium"
                    
                    priority_color = {
                        "high": "🔴",
                        "medium": "🟡",
                        "low": "🟢"
                    }.get(priority, "🟡")
                    
                    title = rec.get("title", rec.get("name", f"Recommendation {idx}"))
                    description = rec.get("description", rec.get("text", rec.get("detail", "")))
                    
                    with st.expander(f"{priority_color} **{title}** (Priority: {priority.title()})"):
                        st.markdown(description if description else "No description provided.")
                elif isinstance(rec, str):
                    # String recommendation - treat as medium priority
                    with st.expander(f"🟡 **Recommendation {idx}** (Priority: Medium)"):
                        st.markdown(rec)
                else:
                    # Unknown format - convert to string
                    with st.expander(f"🟡 **Recommendation {idx}** (Priority: Medium)"):
                        st.markdown(str(rec))
        elif isinstance(recommendations, dict):
            # Single dict recommendation
            priority = recommendations.get("priority", "medium")
            if isinstance(priority, str):
                priority = priority.lower()
            else:
                priority = "medium"
            
            priority_color = {
                "high": "🔴",
                "medium": "🟡",
                "low": "🟢"
            }.get(priority, "🟡")
            
            title = recommendations.get("title", recommendations.get("name", "Recommendation"))
            description = recommendations.get("description", recommendations.get("text", recommendations.get("detail", "")))
            
            with st.expander(f"{priority_color} **{title}** (Priority: {priority.title()})"):
                st.markdown(description if description else "No description provided.")
        else:
            # Unknown format - display as-is
            st.info(f"Recommendations: {str(recommendations)}")
    
    st.markdown("---")
    
    # Category Insights
    if "category_insights" in health_data and health_data["category_insights"]:
        st.markdown("### 📊 Category Insights")
        category_insights = health_data["category_insights"]
        
        # Handle both dict and other formats
        if isinstance(category_insights, dict):
            for category, insight in category_insights.items():
                if isinstance(insight, str):
                    st.markdown(f"**{category}**: {insight}")
                else:
                    st.markdown(f"**{category}**: {str(insight)}")
        elif isinstance(category_insights, list):
            # List format - display as list
            for insight in category_insights:
                if isinstance(insight, dict):
                    category = insight.get("category", insight.get("name", "Unknown"))
                    text = insight.get("insight", insight.get("text", insight.get("description", str(insight))))
                    st.markdown(f"**{category}**: {text}")
                else:
                    st.markdown(f"• {str(insight)}")
        elif isinstance(category_insights, str):
            st.markdown(category_insights)
        else:
            st.markdown(str(category_insights))
        st.markdown("---")
    
    # Key Metrics
    st.markdown("### 📈 Key Financial Metrics")
    metrics = health_data.get("metrics", {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        savings_rate = metrics.get("savings_rate", 0)
        st.metric("Savings Rate", f"{savings_rate:.1f}%")
    
    with col2:
        avg_monthly_net = metrics.get("avg_monthly_income", 0) - metrics.get("avg_monthly_expenses", 0)
        st.metric("Avg Monthly Net", format_currency(avg_monthly_net))
    
    with col3:
        spending_trend = metrics.get("spending_trend", "stable")
        trend_icon = {
            "increasing": "📈",
            "decreasing": "📉",
            "stable": "➡️"
        }.get(spending_trend, "➡️")
        st.metric("Spending Trend", f"{trend_icon} {spending_trend.title()}")
    
    with col4:
        income_consistency = metrics.get("income_consistency", "stable")
        consistency_icon = {
            "consistent": "✅",
            "stable": "➡️",
            "variable": "⚠️"
        }.get(income_consistency, "➡️")
        st.metric("Income Consistency", f"{consistency_icon} {income_consistency.title()}")
    
    # Expenses by Category Chart
    if metrics.get("expenses_by_category"):
        st.markdown("---")
        st.markdown("### 💰 Top Spending Categories (Last 3 Months)")
        
        categories = list(metrics["expenses_by_category"].keys())
        amounts = list(metrics["expenses_by_category"].values())
        
        # Sort by amount
        sorted_data = sorted(zip(categories, amounts), key=lambda x: x[1], reverse=True)
        top_categories = [x[0] for x in sorted_data[:8]]
        top_amounts = [x[1] for x in sorted_data[:8]]
        
        fig = px.bar(
            x=top_amounts,
            y=top_categories,
            orientation='h',
            title="Top Expense Categories",
            labels={"x": "Amount ($)", "y": "Category"},
            color=top_amounts,
            color_continuous_scale="Reds"
        )
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Generated timestamp
    if "generated_at" in health_data:
        generated_time = datetime.fromisoformat(health_data["generated_at"]).strftime("%Y-%m-%d %H:%M:%S")
        st.caption(f"Analysis generated on: {generated_time}")

def show_basic_metrics(data_manager):
    """Show basic financial metrics without AI analysis"""
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    month_summary = data_manager.get_monthly_summary(current_year, current_month)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Monthly Income", format_currency(month_summary["total_income"]))
    with col2:
        st.metric("Monthly Expenses", format_currency(month_summary["total_expenses"]))
    with col3:
        st.metric("Monthly Net", format_currency(month_summary["net"]))
    with col4:
        savings_rate = ((month_summary["total_income"] - month_summary["total_expenses"]) / month_summary["total_income"] * 100) if month_summary["total_income"] > 0 else 0
        st.metric("Savings Rate", f"{savings_rate:.1f}%")

if __name__ == "__main__":
    main()
