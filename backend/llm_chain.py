from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

def chat_with_resume(resume_text, chat_history, user_input):
    system_prompt = f"""
You are a technical interviewer.

Use this resume to guide the interview:
{resume_text}

Rules:
- Ask relevant questions
- Ask follow-ups based on user answers
- Keep it conversational
"""

    messages = [
        {"role": "system", "content": system_prompt},
        *chat_history,
        {"role": "user", "content": user_input},
    ]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
    )

    return response.choices[0].message.content