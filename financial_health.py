"""
Financial Health Score Module
Uses Together.ai to analyze financial data and generate health scores with recommendations
"""
import os
import json
import requests
from typing import Dict, Optional, List
from datetime import datetime


class FinancialHealthAnalyzer:
    """Analyzes financial data and generates health scores using Together.ai"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the analyzer with Together.ai API key
        
        Args:
            api_key: Together.ai API key. If None, will try to get from environment variable TOGETHER_API_KEY
        """
        self.api_key = api_key or os.getenv("TOGETHER_API_KEY")
        self.api_url = "https://api.together.xyz/v1/chat/completions"
        # Default to a serverless model that works with free tier (Build Tier 1) without dedicated endpoints
        # Using Llama 3.3 70B Turbo - Together.ai's default serverless chat model
        self.model = "meta-llama/Llama-3.3-70B-Instruct-Turbo"  # Serverless model - no dedicated endpoint required
        
    def _call_together_ai(self, prompt: str, system_prompt: str = None) -> str:
        """
        Call Together.ai API with a prompt
        
        Args:
            prompt: User prompt
            system_prompt: System prompt for context
            
        Returns:
            AI response text
        """
        if not self.api_key:
            raise ValueError("Together.ai API key is required. Set TOGETHER_API_KEY environment variable or pass api_key parameter.")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1500
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            
            # Check for errors and provide detailed feedback
            if response.status_code != 200:
                error_detail = "Unknown error"
                try:
                    error_response = response.json()
                    error_detail = error_response.get("error", {}).get("message", str(error_response))
                except:
                    error_detail = response.text[:500] if response.text else "No error details provided"
                
                raise Exception(
                    f"Together.ai API error ({response.status_code}): {error_detail}. "
                    f"Model used: {self.model}. "
                    f"Check https://docs.together.ai/docs/models for available models."
                )
            
            result = response.json()
            
            # Validate response structure
            if "choices" not in result or len(result["choices"]) == 0:
                raise Exception("Empty response from Together.ai API")
            
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            # Extract more details from the error
            error_msg = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    error_msg = f"{error_msg} - Details: {error_detail}"
                except:
                    error_msg = f"{error_msg} - Response: {e.response.text[:200]}"
            raise Exception(f"Error calling Together.ai API: {error_msg}")
        except (KeyError, IndexError) as e:
            raise Exception(f"Unexpected response format from Together.ai: {str(e)}")
    
    def calculate_financial_metrics(self, data_manager) -> Dict:
        """
        Calculate financial metrics from user data
        
        Args:
            data_manager: DataManager instance
            
        Returns:
            Dictionary with calculated metrics
        """
        income_df = data_manager.get_income_df()
        expenses_df = data_manager.get_expenses_df()
        
        # Get current date info
        now = datetime.now()
        current_month = now.month
        current_year = now.year
        
        # Calculate time ranges
        last_3_months = []
        for i in range(3):
            month = current_month - i
            year = current_year
            if month <= 0:
                month += 12
                year -= 1
            last_3_months.append((year, month))
        
        # Overall totals
        total_income = income_df["amount"].sum() if not income_df.empty else 0
        total_expenses = expenses_df["amount"].sum() if not expenses_df.empty else 0
        
        # Current month metrics
        current_month_income = 0
        current_month_expenses = 0
        if not income_df.empty:
            current_month_income = income_df[
                (income_df["date"].dt.year == current_year) & 
                (income_df["date"].dt.month == current_month)
            ]["amount"].sum()
        
        if not expenses_df.empty:
            current_month_expenses = expenses_df[
                (expenses_df["date"].dt.year == current_year) & 
                (expenses_df["date"].dt.month == current_month)
            ]["amount"].sum()
        
        # Last 3 months average
        avg_monthly_income = 0
        avg_monthly_expenses = 0
        monthly_data = []
        
        for year, month in last_3_months:
            month_income = 0
            month_expenses = 0
            
            if not income_df.empty:
                month_income = income_df[
                    (income_df["date"].dt.year == year) & 
                    (income_df["date"].dt.month == month)
                ]["amount"].sum()
            
            if not expenses_df.empty:
                month_expenses = expenses_df[
                    (expenses_df["date"].dt.year == year) & 
                    (expenses_df["date"].dt.month == month)
                ]["amount"].sum()
            
            monthly_data.append({
                "year": year,
                "month": month,
                "income": month_income,
                "expenses": month_expenses,
                "net": month_income - month_expenses
            })
            
            avg_monthly_income += month_income
            avg_monthly_expenses += month_expenses
        
        if len(monthly_data) > 0:
            avg_monthly_income /= len(monthly_data)
            avg_monthly_expenses /= len(monthly_data)
        
        # Savings rate
        savings_rate = 0
        if current_month_income > 0:
            savings_rate = ((current_month_income - current_month_expenses) / current_month_income) * 100
        
        # Expenses by category (last 3 months)
        expenses_by_category = {}
        if not expenses_df.empty:
            last_3_months_dates = []
            for year, month in last_3_months:
                last_3_months_dates.append((year, month))
            
            recent_expenses = expenses_df[
                expenses_df.apply(
                    lambda row: (row["date"].year, row["date"].month) in last_3_months_dates,
                    axis=1
                )
            ]
            
            if not recent_expenses.empty:
                expenses_by_category = recent_expenses.groupby("category")["amount"].sum().to_dict()
        
        # Spending trends
        spending_trend = "stable"
        if len(monthly_data) >= 2:
            recent_expenses = [m["expenses"] for m in monthly_data[:2]]
            if recent_expenses[0] > recent_expenses[1] * 1.1:
                spending_trend = "increasing"
            elif recent_expenses[0] < recent_expenses[1] * 0.9:
                spending_trend = "decreasing"
        
        # Income consistency
        income_consistency = "stable"
        if len(monthly_data) >= 2:
            recent_income = [m["income"] for m in monthly_data[:2]]
            income_variance = abs(recent_income[0] - recent_income[1]) / max(recent_income) if max(recent_income) > 0 else 0
            if income_variance > 0.2:
                income_consistency = "variable"
            elif income_variance < 0.05:
                income_consistency = "consistent"
        
        # Number of transactions
        num_income_transactions = len(income_df) if not income_df.empty else 0
        num_expense_transactions = len(expenses_df) if not expenses_df.empty else 0
        
        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "current_month_income": current_month_income,
            "current_month_expenses": current_month_expenses,
            "avg_monthly_income": avg_monthly_income,
            "avg_monthly_expenses": avg_monthly_expenses,
            "savings_rate": savings_rate,
            "expenses_by_category": expenses_by_category,
            "spending_trend": spending_trend,
            "income_consistency": income_consistency,
            "monthly_data": monthly_data,
            "num_income_transactions": num_income_transactions,
            "num_expense_transactions": num_expense_transactions,
            "data_span_months": len(monthly_data)
        }
    
    def generate_health_score(self, data_manager) -> Dict:
        """
        Generate comprehensive financial health score using AI
        
        Args:
            data_manager: DataManager instance
            
        Returns:
            Dictionary with score, analysis, and recommendations
        """
        # Calculate metrics
        metrics = self.calculate_financial_metrics(data_manager)
        
        # Prepare data for AI analysis
        financial_summary = {
            "current_month": {
                "income": metrics["current_month_income"],
                "expenses": metrics["current_month_expenses"],
                "net": metrics["current_month_income"] - metrics["current_month_expenses"],
                "savings_rate": metrics["savings_rate"]
            },
            "average_monthly": {
                "income": metrics["avg_monthly_income"],
                "expenses": metrics["avg_monthly_expenses"],
                "net": metrics["avg_monthly_income"] - metrics["avg_monthly_expenses"]
            },
            "total": {
                "income": metrics["total_income"],
                "expenses": metrics["total_expenses"],
                "net": metrics["total_income"] - metrics["total_expenses"]
            },
            "trends": {
                "spending_trend": metrics["spending_trend"],
                "income_consistency": metrics["income_consistency"]
            },
            "expenses_by_category": metrics["expenses_by_category"],
            "monthly_breakdown": metrics["monthly_data"],
            "transaction_count": {
                "income": metrics["num_income_transactions"],
                "expenses": metrics["num_expense_transactions"]
            }
        }
        
        # Create system prompt
        system_prompt = """You are a financial advisor AI assistant. Analyze the provided financial data and generate:
1. A financial health score from 0-100 (where 100 is excellent)
2. A brief analysis of the financial situation
3. 3-5 specific, actionable recommendations for improvement

Consider factors like:
- Savings rate (aim for 20%+)
- Spending trends (increasing/decreasing/stable)
- Income consistency
- Category spending distribution
- Overall financial stability

Be encouraging but honest. Provide practical, actionable advice."""
        
        # Create user prompt with financial data
        user_prompt = f"""Please analyze the following financial data and provide a comprehensive financial health assessment:

Financial Summary:
{json.dumps(financial_summary, indent=2)}

Please provide your response in the following JSON format:
{{
    "score": <number between 0-100>,
    "score_explanation": "<brief explanation of the score>",
    "analysis": "<2-3 paragraph analysis of the financial situation>",
    "strengths": ["<strength 1>", "<strength 2>", ...],
    "concerns": ["<concern 1>", "<concern 2>", ...],
    "recommendations": [
        {{
            "priority": "<high/medium/low>",
            "title": "<recommendation title>",
            "description": "<detailed recommendation>"
        }},
        ...
    ],
    "category_insights": {{
        "<category>": "<insight about this category>",
        ...
    }}
}}

Focus on providing actionable, personalized advice based on the actual spending patterns."""
        
        try:
            # Call Together.ai
            ai_response = self._call_together_ai(user_prompt, system_prompt)
            
            # Try to parse JSON from response
            # Sometimes AI wraps JSON in markdown code blocks
            if "```json" in ai_response:
                json_start = ai_response.find("```json") + 7
                json_end = ai_response.find("```", json_start)
                ai_response = ai_response[json_start:json_end].strip()
            elif "```" in ai_response:
                json_start = ai_response.find("```") + 3
                json_end = ai_response.find("```", json_start)
                ai_response = ai_response[json_start:json_end].strip()
            
            # Parse JSON response
            try:
                health_data = json.loads(ai_response)
            except json.JSONDecodeError:
                # If JSON parsing fails, create a structured response from text
                health_data = {
                    "score": 70,  # Default score
                    "score_explanation": "Based on standard financial metrics",
                    "analysis": ai_response[:500] if len(ai_response) > 500 else ai_response,
                    "strengths": [],
                    "concerns": [],
                    "recommendations": [
                        {
                            "priority": "medium",
                            "title": "Review AI Analysis",
                            "description": ai_response
                        }
                    ],
                    "category_insights": {}
                }
            
            # Ensure score is within valid range
            if "score" in health_data:
                health_data["score"] = max(0, min(100, int(health_data.get("score", 70))))
            else:
                health_data["score"] = 70
            
            # Add metrics to response
            health_data["metrics"] = metrics
            health_data["generated_at"] = datetime.now().isoformat()
            
            return health_data
            
        except Exception as e:
            # Fallback response if AI call fails
            return {
                "score": self._calculate_fallback_score(metrics),
                "score_explanation": "Calculated using standard financial metrics",
                "analysis": f"Unable to generate AI analysis: {str(e)}. Using fallback calculation.",
                "strengths": self._get_fallback_strengths(metrics),
                "concerns": self._get_fallback_concerns(metrics),
                "recommendations": self._get_fallback_recommendations(metrics),
                "category_insights": {},
                "metrics": metrics,
                "generated_at": datetime.now().isoformat(),
                "error": str(e)
            }
    
    def _calculate_fallback_score(self, metrics: Dict) -> int:
        """Calculate a fallback score if AI is unavailable"""
        score = 50  # Base score
        
        # Savings rate contribution (0-30 points)
        savings_rate = metrics.get("savings_rate", 0)
        if savings_rate >= 20:
            score += 30
        elif savings_rate >= 10:
            score += 20
        elif savings_rate >= 5:
            score += 10
        elif savings_rate < 0:
            score -= 20
        
        # Spending trend contribution (0-20 points)
        spending_trend = metrics.get("spending_trend", "stable")
        if spending_trend == "decreasing":
            score += 20
        elif spending_trend == "stable":
            score += 10
        else:
            score -= 10
        
        # Income consistency (0-20 points)
        income_consistency = metrics.get("income_consistency", "stable")
        if income_consistency == "consistent":
            score += 20
        elif income_consistency == "stable":
            score += 10
        
        # Expense distribution (0-10 points) - more categories = better tracking
        num_categories = len(metrics.get("expenses_by_category", {}))
        if num_categories >= 5:
            score += 10
        elif num_categories >= 3:
            score += 5
        
        # Data completeness (0-10 points)
        total_transactions = metrics.get("num_income_transactions", 0) + metrics.get("num_expense_transactions", 0)
        if total_transactions >= 20:
            score += 10
        elif total_transactions >= 10:
            score += 5
        
        return max(0, min(100, score))
    
    def _get_fallback_strengths(self, metrics: Dict) -> List[str]:
        """Get fallback strengths based on metrics"""
        strengths = []
        
        savings_rate = metrics.get("savings_rate", 0)
        if savings_rate > 0:
            strengths.append(f"Positive savings rate of {savings_rate:.1f}%")
        
        if metrics.get("spending_trend") == "decreasing":
            strengths.append("Spending is trending downward")
        
        if metrics.get("income_consistency") == "consistent":
            strengths.append("Stable and consistent income")
        
        if len(metrics.get("expenses_by_category", {})) >= 5:
            strengths.append("Good expense categorization and tracking")
        
        return strengths if strengths else ["Starting to track your finances"]
    
    def _get_fallback_concerns(self, metrics: Dict) -> List[str]:
        """Get fallback concerns based on metrics"""
        concerns = []
        
        savings_rate = metrics.get("savings_rate", 0)
        if savings_rate < 0:
            concerns.append("Spending exceeds income - negative savings rate")
        elif savings_rate < 5:
            concerns.append("Low savings rate - aim for at least 20%")
        
        if metrics.get("spending_trend") == "increasing":
            concerns.append("Spending trend is increasing")
        
        if metrics.get("income_consistency") == "variable":
            concerns.append("Income is highly variable")
        
        return concerns
    
    def _get_fallback_recommendations(self, metrics: Dict) -> List[Dict]:
        """Get fallback recommendations based on metrics"""
        recommendations = []
        
        savings_rate = metrics.get("savings_rate", 0)
        if savings_rate < 20:
            recommendations.append({
                "priority": "high",
                "title": "Increase Savings Rate",
                "description": f"Your current savings rate is {savings_rate:.1f}%. Aim to save at least 20% of your income. Review your expenses and identify areas where you can cut back."
            })
        
        if metrics.get("spending_trend") == "increasing":
            recommendations.append({
                "priority": "high",
                "title": "Control Spending Growth",
                "description": "Your spending has been increasing. Review your recent expenses and identify unnecessary purchases. Set a monthly spending limit."
            })
        
        top_category = max(metrics.get("expenses_by_category", {}).items(), key=lambda x: x[1], default=None)
        # Compare 3-month category total against 30% of 3-month total expenses
        # avg_monthly_expenses * 3 * 0.3 = avg_monthly_expenses * 0.9
        if top_category and top_category[1] > metrics.get("avg_monthly_expenses", 0) * 0.9:
            recommendations.append({
                "priority": "medium",
                "title": f"Review {top_category[0]} Spending",
                "description": f"{top_category[0]} accounts for a significant portion of your expenses. Consider if this spending aligns with your financial goals."
            })
        
        if len(metrics.get("expenses_by_category", {})) < 3:
            recommendations.append({
                "priority": "low",
                "title": "Improve Expense Tracking",
                "description": "Categorize more of your expenses to get better insights into your spending patterns."
            })
        
        return recommendations if recommendations else [{
            "priority": "medium",
            "title": "Continue Tracking",
            "description": "Keep tracking your expenses regularly to build a comprehensive financial picture."
        }]
