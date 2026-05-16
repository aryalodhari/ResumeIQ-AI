from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# Load .env file
load_dotenv()

# Read API key
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def analyze_resume(resume_text, user_goal):

    prompt = f"""
You are a senior software engineer and hiring manager.

Evaluate the resume based on the user's goal.

User goal: "{user_goal}"

STRICT RULES:
- Extract only relevant skills for this goal
- Remove irrelevant tools
- Identify real gaps
- Generate roadmap only for missing fields
- Make output different based on goal

Return JSON only:

{{
    "skills": [],
    "missing_skills": [],
    "roadmap": [],
    "interview_questions": []
}}

Resume:
{resume_text}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            temperature=0.3,
            messages=[
                {
                    "role": "system",
                    "content": "You are a strict hiring manager."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response.choices[0].message.content.strip()

        # Convert AI output into Python dictionary
        result = json.loads(content)

        return result

    except Exception as e:
        return {
            "skills": [],
            "missing_skills": [],
            "roadmap": [],
            "interview_questions": [],
            "error": str(e)
        }