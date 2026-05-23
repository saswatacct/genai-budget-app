import os
from groq import Groq
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Initialize Groq client with API key from environment
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_financial_suggestion(
    data
):

    prompt = f"""
    You are a smart fintech AI assistant.

    Analyze the user's spending pattern.

    Total Limit:
    ₹{data['total_limit']}

    Remaining Limit:
    ₹{data['remaining']}

    Average Daily Spend:
    ₹{data['avg_daily']}

    Days Remaining:
    {data['days_left']}

    Rules:
    - Response must be maximum 2 lines only
    - Keep response concise
    - Give practical financial advice
    - No headings
    - No bullet points
    - WhatsApp friendly tone
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=60
    )

    return response.choices[0].message.content.strip()