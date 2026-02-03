# Financial Health Score Setup Guide

The Financial Health Score feature uses Together.ai to provide AI-powered analysis of your financial situation.

## Prerequisites

1. **Together.ai API Key**: Get your free API key from [https://api.together.xyz/](https://api.together.xyz/)
   - Sign up for an account
   - Navigate to API Keys section
   - Create a new API key

## Setup Options

### Option 1: Environment Variable (Recommended)

**Windows PowerShell:**
```powershell
$env:TOGETHER_API_KEY="your-api-key-here"
streamlit run app.py
```

**Windows CMD:**
```cmd
set TOGETHER_API_KEY=your-api-key-here
streamlit run app.py
```

**macOS/Linux:**
```bash
export TOGETHER_API_KEY=your-api-key-here
streamlit run app.py
```

**Permanent Setup (Windows):**
1. Open System Properties → Environment Variables
2. Add new User Variable:
   - Name: `TOGETHER_API_KEY`
   - Value: `your-api-key-here`

**Permanent Setup (macOS/Linux):**
Add to your `~/.bashrc` or `~/.zshrc`:
```bash
export TOGETHER_API_KEY="your-api-key-here"
```

### Option 2: Streamlit Secrets (For Production)

1. Create a `.streamlit` directory in your project root (if it doesn't exist)
2. Create a `secrets.toml` file inside `.streamlit/`
3. Add your API key:
```toml
TOGETHER_API_KEY = "your-api-key-here"
```

**Note:** Add `.streamlit/secrets.toml` to `.gitignore` to keep your API key secure!

## Usage

1. Start the application: `streamlit run app.py`
2. Log in to your account
3. Navigate to **"💚 Financial Health"** in the navigation bar
4. Click **"🔄 Refresh Analysis"** to generate your financial health score
5. Review your score, analysis, and personalized recommendations

## Features

- **AI-Powered Score (0-100)**: Comprehensive financial health assessment
- **Detailed Analysis**: AI-generated insights into your financial situation
- **Strengths & Concerns**: Identify what you're doing well and areas to improve
- **Personalized Recommendations**: Actionable advice tailored to your spending patterns
- **Category Insights**: Analysis of spending by category
- **Key Metrics**: Savings rate, spending trends, income consistency

## Troubleshooting

### "API Key Required" Warning
- Make sure you've set the `TOGETHER_API_KEY` environment variable
- Restart your terminal/command prompt after setting the variable
- Verify the key is correct (no extra spaces)

### 400 Bad Request Error
This is the most common error. It usually means:

1. **"Non-serverless model" error** - The model requires a dedicated endpoint
   - **Solution**: Select a serverless model from the dropdown:
     - Start with **"meta-llama/Llama-2-7b-chat-hf"** (recommended for free tier)
     - Or try "meta-llama/Llama-2-70b-chat-hf" or "mistralai/Mistral-7B-Instruct-v0.1"
   - Serverless models work with free/starter accounts without needing dedicated endpoints
   - Check serverless models at: https://together.ai/models (filter for serverless)

2. **Model not available** - The selected model might not be available on your Together.ai plan
   - **Solution**: Try selecting a different model from the dropdown
   - Check available models at: https://together.ai/models

3. **Invalid API key** - Your API key might be incorrect
   - **Solution**: Verify your key at https://api.together.xyz/

4. **Insufficient credits** - Your account might not have enough credits
   - **Solution**: Check your Together.ai account balance

### 401 Unauthorized Error
- Your API key is invalid or expired
- **Solution**: Generate a new API key from your Together.ai dashboard

### 429 Rate Limit Error
- You've made too many requests too quickly
- **Solution**: Wait a few moments and try again

### Other API Errors
- Check your Together.ai account has available credits
- Verify your API key is valid
- Check your internet connection
- The app will show basic metrics if AI analysis fails

### Slow Response
- AI analysis may take 10-30 seconds depending on data size
- The analysis is cached in your session - refresh only when needed
- Larger models (70B) take longer but provide better analysis

## Security Notes

- Never commit your API key to version control
- Keep your API key private and secure
- The API key is only used to call Together.ai - your financial data stays local

## Cost Information

- Together.ai offers free tier with limited requests
- Check [Together.ai pricing](https://www.together.ai/pricing) for current rates
- Each health score generation uses one API call
