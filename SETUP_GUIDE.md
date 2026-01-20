# Setup Guide - Personal Expense Tracker

This guide will help you set up the Personal Expense Tracker application on your local machine.

## Prerequisites

Before you begin, make sure you have the following installed on your computer:

1. **Python 3.7 or higher**
   - Check if Python is installed: Open terminal/command prompt and run `python --version` or `python3 --version`
   - If not installed, download from [python.org](https://www.python.org/downloads/)
   - **Important**: During installation, check "Add Python to PATH"

2. **Git** (optional, for cloning the repository)
   - Download from [git-scm.com](https://git-scm.com/downloads)

## Step-by-Step Setup Instructions

### Step 1: Get the Project Files

**Option A: Clone from GitHub (Recommended)**
```bash
git clone <repository-url>
cd expense_tracker
```

**Option B: Download as ZIP**
1. Download the project ZIP file from GitHub
2. Extract it to a folder on your computer
3. Open terminal/command prompt and navigate to the extracted folder:
   ```bash
   cd path/to/expense_tracker
   ```

### Step 2: Create a Virtual Environment (Recommended)

Creating a virtual environment isolates the project dependencies from other Python projects on your system.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the beginning of your command prompt, indicating the virtual environment is active.

### Step 3: Install Required Packages

With your virtual environment activated, install all required dependencies:

```bash
pip install -r requirements.txt
```

This will install:
- streamlit (web framework)
- pandas (data manipulation)
- plotly (interactive charts)
- openpyxl (Excel file support)

**Troubleshooting:**
- If `pip` is not recognized, try `pip3` instead
- If you get permission errors, make sure your virtual environment is activated
- On some systems, you may need to use `python -m pip install -r requirements.txt`

### Step 4: Verify Installation

Check that all packages are installed correctly:

```bash
pip list
```

You should see streamlit, pandas, plotly, and openpyxl in the list.

### Step 5: Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

**What happens next:**
- Streamlit will start a local web server
- Your default web browser should automatically open
- If it doesn't, look for a message like: "You can now view your Streamlit app in your browser. Local URL: http://localhost:8501"
- Copy that URL and paste it into your browser

### Step 6: Create Your Account

1. You'll see the login page
2. Click "Don't have an account? Register here"
3. Fill in the registration form:
   - **Username**: Choose a unique username (minimum 3 characters)
   - **Password**: Create a password (minimum 6 characters)
   - **Confirm Password**: Re-enter your password
   - **Email** (optional): Your email address
   - **Full Name** (optional): Your name
4. Click "Register"
5. After successful registration, you'll be redirected to the login page
6. Log in with your new credentials

## Running the Application

### Starting the App

1. Open terminal/command prompt
2. Navigate to the project directory:
   ```bash
   cd path/to/expense_tracker
   ```
3. Activate virtual environment (if not already active):
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Run the application:
   ```bash
   streamlit run app.py
   ```

### Stopping the App

- Press `Ctrl + C` in the terminal/command prompt where Streamlit is running
- Or simply close the terminal window

## Troubleshooting

### Issue: "streamlit: command not found"

**Solution:**
- Make sure your virtual environment is activated
- Try: `python -m streamlit run app.py` or `python3 -m streamlit run app.py`

### Issue: Port 8501 is already in use

**Solution:**
- Another Streamlit app might be running
- Stop other Streamlit processes or use a different port:
  ```bash
  streamlit run app.py --server.port 8502
  ```

### Issue: Module not found errors

**Solution:**
- Make sure you installed requirements: `pip install -r requirements.txt`
- Verify virtual environment is activated
- Try reinstalling: `pip install --upgrade -r requirements.txt`

### Issue: Browser doesn't open automatically

**Solution:**
- Look for the URL in the terminal (usually `http://localhost:8501`)
- Copy and paste it into your browser manually

### Issue: Can't see my data after restarting

**Solution:**
- Data is stored locally in JSON files
- Make sure you're logged in with the same username
- Check that `expense_data_<your_username>.json` exists in the project folder

## Project Structure

After setup, your project folder should look like this:

```
expense_tracker/
├── app.py                 # Main application file
├── auth_manager.py        # Authentication module
├── data_manager.py        # Data management module
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── SETUP_GUIDE.md         # This file
├── .gitignore            # Git ignore rules
├── venv/                 # Virtual environment (created during setup)
├── users.json            # User accounts (created after first registration)
└── expense_data_*.json   # User expense data (created after adding transactions)
```

## Next Steps

Once the application is running:

1. **Add Your First Transaction**: Go to "Add Transaction" and enter an income or expense
2. **Explore Visualizations**: Check out "Monthly Summary" and "Yearly Summary" for charts and graphs
3. **Manage Your Profile**: Visit "Profile" to update your account information
4. **Export Your Data**: Use "Settings" to export your data to CSV

## Getting Help

If you encounter issues:

1. Check this setup guide for common problems
2. Review the main README.md for feature documentation
3. Check that all prerequisites are installed correctly
4. Verify your virtual environment is activated
5. Ensure all dependencies are installed: `pip list`

## Development Notes

- **Data Storage**: All data is stored locally in JSON files
- **No Database Required**: The app uses file-based storage
- **User Isolation**: Each user's data is stored separately
- **Security**: Passwords are hashed before storage

## Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python Virtual Environments Guide](https://docs.python.org/3/tutorial/venv.html)
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)

---

**Happy Tracking!** 💰📊
