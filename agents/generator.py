import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class GeneratorAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def generate(self, grade, topic, feedback=None):
        base_prompt = f"""
You are an educational content generator.

STRICT INSTRUCTIONS:
- Output ONLY valid JSON
- No markdown, no extra text
- EXACTLY 3 MCQs
- Each MCQ must have 4 meaningful options
- Answer must be one of the options

Grade: {grade}
Topic: {topic}

Return:
{{
  "explanation": "string",
  "mcqs": [
    {{
      "question": "string",
      "options": ["opt1","opt2","opt3","opt4"],
      "answer": "string"
    }},
    {{
      "question": "string",
      "options": ["opt1","opt2","opt3","opt4"],
      "answer": "string"
    }},
    {{
      "question": "string",
      "options": ["opt1","opt2","opt3","opt4"],
      "answer": "string"
    }}
  ]
}}
"""

        if feedback:
            base_prompt += f"\nImprove based on: {feedback}"

        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": base_prompt}],
                temperature=0.3
            )

            raw = response.choices[0].message.content.strip()

            # Extract JSON
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if not match:
                raise ValueError("No JSON found")

            data = json.loads(match.group(0))

            # -------------------------------
            # Enforce key order for MCQs
            # -------------------------------
            formatted_mcqs = []
            for mcq in data.get("mcqs", []):
                formatted_mcqs.append({
                    "question": mcq.get("question", ""),
                    "options": mcq.get("options", []),
                    "answer": mcq.get("answer", "")
                })

            data["mcqs"] = formatted_mcqs

            # -------------------------------
            # Validation
            # -------------------------------
            if "explanation" not in data or "mcqs" not in data:
                raise ValueError("Invalid structure")

            if len(data["mcqs"]) != 3:
                raise ValueError("Wrong MCQ count")

            return data

        except Exception as e:
            print("Generator Error:", e)

            # Fallback
            return {
                "explanation": f"Basic explanation of {topic}.",
                "mcqs": [
                    {
                        "question": f"What is {topic}?",
                        "options": ["Concept", "Number", "Process", "Object"],
                        "answer": "Concept"
                    }
                ]
            }