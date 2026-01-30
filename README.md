# 💰 Personal Expense Tracker

A comprehensive web-based application for tracking personal income and expenses with detailed monthly and yearly summaries, featuring multiple visualization formats. Includes user authentication, profile management, and secure data storage.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### 🔐 Authentication & User Management
- **User Registration**: Create a new account with username and password
- **Secure Login**: Password-protected access to your personal data
- **User Profiles**: Manage your account information and preferences
- **User-Specific Data**: Each user's data is stored separately and securely
- **Password Management**: Change your password securely

### 💵 Financial Tracking
- **Income Tracking**: Record income from various sources with dates and descriptions
- **Expense Tracking**: Categorize and track expenses across 12 predefined categories
- **Transaction Management**: View, add, and delete income and expense entries
- **Quick Overview**: Dashboard with current month statistics

### 📊 Monthly Summary
- Summary cards (income, expenses, net amount, savings rate)
- Pie charts for expense distribution by category
- Bar charts for category comparisons
- Detailed transaction tables
- Month and year selection

### 📈 Yearly Summary
- Monthly trend line charts (income vs expenses)
- Yearly expense distribution pie charts
- Top expense categories horizontal bar charts
- Monthly income vs expenses comparison bar charts
- Summary statistics table
- Year selection

### 👤 User Profile
- Update account information (email, full name)
- Change password securely
- Customize preferences (currency, date format, theme)

### ⚙️ Additional Features
- **Data Export**: Export your data to CSV format
- **All Transactions View**: Comprehensive list of all income and expenses
- **Responsive Design**: Works on desktop and tablet devices
- **Interactive Charts**: Powered by Plotly for dynamic visualizations

## 🖼️ Screenshots

*Note: Add screenshots of your application here*

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Git (optional, for cloning)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Personal-Expense-Tracker
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

**For detailed setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)**

## 🏃 Quick Start

1. **Register an Account**
   - Open the application
   - Click "Don't have an account? Register here"
   - Fill in your details and register

2. **Login**
   - Enter your username and password
   - Click "Login"

3. **Add Your First Transaction**
   - Navigate to "Add Transaction"
   - Enter an income or expense
   - Click "Add Income" or "Add Expense"

4. **View Your Summary**
   - Check "Monthly Summary" for current month breakdown
   - Explore "Yearly Summary" for annual trends

## 📖 Usage

### Adding Transactions

1. Go to **Add Transaction** page
2. Fill in the form:
   - **Amount**: Enter the dollar amount
   - **Date**: Select the transaction date
   - **Source/Category**: Enter source (income) or select category (expense)
   - **Description**: Add optional notes
3. Click the submit button

### Viewing Summaries

- **Monthly Summary**: Select year and month, view charts and tables
- **Yearly Summary**: Select year, view trends and annual breakdown
- **All Transactions**: See complete list of all entries

### Managing Profile

1. Go to **Profile** page
2. Update account information
3. Change password if needed
4. Customize preferences (currency, date format, theme)

### Exporting Data

1. Go to **Settings** page
2. Click "Export to CSV"
3. Download your data file

## 📁 Project Structure

```
expense_tracker/
├── app.py                 # Main Streamlit application
├── auth_manager.py         # Authentication and user management
├── data_manager.py         # Data storage and retrieval
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── SETUP_GUIDE.md         # Detailed setup instructions
├── .gitignore            # Git ignore rules
├── users.json            # User accounts (created at runtime)
└── expense_data_*.json    # User expense data (created at runtime)
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Data Processing**: Pandas
- **Visualizations**: Plotly
- **Data Storage**: JSON files
- **Authentication**: Custom implementation with SHA-256 hashing

### Dependencies

- `streamlit==1.28.0` - Web framework
- `pandas==2.1.3` - Data manipulation
- `plotly==5.18.0` - Interactive charts
- `openpyxl==3.1.2` - Excel file support

## 🔒 Security

- **Password Hashing**: Passwords are hashed using SHA-256 before storage
- **User Isolation**: Each user's financial data is stored in separate files
- **Session Management**: Secure session handling for authenticated users
- **Local Storage**: All data is stored locally on your machine
- **No External Services**: No data is sent to external servers

### Security Best Practices

- Never share your login credentials
- Keep your data files secure
- Use strong passwords (minimum 6 characters, but longer is better)
- Regularly export your data as backup

## 📊 Expense Categories

The application includes 12 predefined expense categories:

- Food & Dining
- Transportation
- Shopping
- Bills & Utilities
- Entertainment
- Healthcare
- Education
- Travel
- Personal Care
- Gifts & Donations
- Housing
- Other

## 💾 Data Storage

### User Data
- **User Accounts**: Stored in `users.json`
- **Financial Data**: Each user's data in `expense_data_<username>.json`
- **Format**: JSON files for easy backup and portability

### Backup Recommendations

1. Regularly export your data to CSV (Settings page)
2. Backup the JSON files from the project directory
3. Store backups in a secure location

## 🐛 Troubleshooting

### Common Issues

**Port already in use:**
```bash
streamlit run app.py --server.port 8502
```

**Module not found:**
```bash
pip install --upgrade -r requirements.txt
```

**Can't see data:**
- Ensure you're logged in with the correct username
- Check that data files exist in the project directory

For more troubleshooting help, see [SETUP_GUIDE.md](SETUP_GUIDE.md)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

1. Follow the installation steps above
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👥 Authors

- **Your Name** - *Initial work*

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- Plotly for interactive charting capabilities
- Pandas for powerful data manipulation

## 📞 Support

If you encounter any issues or have questions:

1. Check the [SETUP_GUIDE.md](SETUP_GUIDE.md) for common solutions
2. Review existing issues on GitHub
3. Create a new issue with detailed information

---

**Made with ❤️ for better financial tracking**

