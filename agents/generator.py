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

        prompt = f"""
You are an educational content generator.

STRICT RULES:
- Output ONLY valid JSON
- EXACTLY 3 MCQs
- Each MCQ must have 4 options
- Answer must EXACTLY match one of the options (not A/B/C/D)
- Do NOT generate extra questions
- Do NOT merge questions
- Keep questions clean and separate
- Do NOT ask diagram/figure-based questions
- Stay strictly on topic
- Adjust difficulty based on grade

Grade: {grade}
Topic: {topic}

Return format:
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
            prompt += f"\nFix issues: {feedback}"

        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )

            raw = response.choices[0].message.content.strip()

            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if not match:
                raise ValueError("No JSON")

            data = json.loads(match.group(0))

            # 🔥 Clean + normalize MCQs
            cleaned_mcqs = []

            for mcq in data.get("mcqs", []):
                question = mcq.get("question", "").strip()
                options = [opt.strip() for opt in mcq.get("options", [])]
                answer = mcq.get("answer", "").strip()

                # Fix answer mismatch (if AI returns A/B/C/D)
                if answer in ["A", "B", "C", "D"]:
                    idx = ["A", "B", "C", "D"].index(answer)
                    if idx < len(options):
                        answer = options[idx]

                # Ensure answer exists in options
                if answer not in options and options:
                    answer = options[0]

                cleaned_mcqs.append({
                    "question": question,
                    "options": options,
                    "answer": answer
                })

            data["mcqs"] = cleaned_mcqs[:3]  # force 3 only

            if len(data["mcqs"]) != 3:
                raise ValueError("Invalid MCQs")

            return data

        except Exception as e:
            print("Generator Error:", e)

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