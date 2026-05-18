from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def analyze_resume(resume_text, user_goal):

    prompt = f"""
You are a senior software engineer and hiring manager.

Evaluate the resume based on the user's goal.

User Goal: "{user_goal}"

STRICT RULES:
- Extract only relevant skills
- Remove irrelevant tools
- Identify real gaps
- Generate roadmap only for missing skills
- Generate interview questions

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

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        content = response.text.strip()

        # Remove markdown formatting if present
        content = content.replace("```json", "")
        content = content.replace("```", "")

        return json.loads(content)

    except Exception as e:

        return {
            "skills": [],
            "missing_skills": [],
            "roadmap": [],
            "interview_questions": [],
            "error": str(e)
        }