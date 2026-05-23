from datetime import datetime


def build_message(data):

    current_time = datetime.now().strftime(
        "%d-%m-%Y %I:%M %p"
    )

    return f"""
👋 Hello {data["user_name"]},

💳 *SmartSpend AI Financial Alert Created by Mr.Saswat*

━━━━━━━━━━━━━━━━━━

📅 Current Billing Cycle:
{data["billing_cycle"]}

💰 Set UPI Limit:
₹{data["upi_limit"]}

💳 Set Credit Card Limit:
₹{data["credit_limit"]}

━━━━━━━━━━━━━━━━━━

🕒 Transaction Added At:
{current_time}

💵 Recent Transaction Amount Added:
₹{data["amount"]}

🏪 Merchant:
{data["merchant"]}

💳 Transaction Mode:
{data["txn_mode"]}

━━━━━━━━━━━━━━━━━━

🏧 ATM Usage:
{"Enabled" if data["atm_flag"] else "Disabled"}

🌐 Online Usage:
{"Enabled" if data["online_flag"] else "Disabled"}

━━━━━━━━━━━━━━━━━━

📊 Average Spend Per Day:
₹{data["avg_daily"]}

⚠️ Alert:
{data["alert"] if data["alert"] else "No Alerts"}

━━━━━━━━━━━━━━━━━━

🤖 AI Financial Suggestion:

{data["suggestion"]}

━━━━━━━━━━━━━━━━━━

🙏 Thank you for using SmartSpend AI.
Stay financially healthy 💙
"""