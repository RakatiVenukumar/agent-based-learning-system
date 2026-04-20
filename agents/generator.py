import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeneratorAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def generate(self, grade, topic, feedback=None):
        """
        Generates educational content using Groq AI
        """

        # -------------------------------
        # Prompt Design (VERY IMPORTANT)
        # -------------------------------
        base_prompt = f"""
You are an educational content generator.

Generate content for:
Grade: {grade}
Topic: {topic}

Rules:
- Language must match grade level
- Keep explanation clear and correct
- Generate exactly 3 MCQs
- Each MCQ must have 4 options
- Include correct answer

Return ONLY valid JSON in this format:
{{
  "explanation": "...",
  "mcqs": [
    {{
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "answer": "..."
    }}
  ]
}}
"""

        # Add refinement if feedback exists
        if feedback:
            base_prompt += f"""

Improve the content based on this feedback:
{feedback}

Make it simpler and clearer.
"""

        try:
            # -------------------------------
            # Call Groq API
            # -------------------------------
            response = self.client.chat.completions.create(
                model="llama3-70b-8192",  # strong + fast
                messages=[
                    {"role": "user", "content": base_prompt}
                ],
                temperature=0.3  # low randomness = stable output
            )

            raw_output = response.choices[0].message.content.strip()

            # -------------------------------
            # Extract JSON safely
            # -------------------------------
            start = raw_output.find("{")
            end = raw_output.rfind("}") + 1
            json_str = raw_output[start:end]

            parsed_output = json.loads(json_str)

            # -------------------------------
            # Basic structure validation
            # -------------------------------
            if "explanation" not in parsed_output or "mcqs" not in parsed_output:
                raise ValueError("Invalid structure")

            return parsed_output

        except Exception as e:
            # -------------------------------
            # Fallback (VERY IMPORTANT)
            # -------------------------------
            return {
                "explanation": f"Basic explanation of {topic} for grade {grade}.",
                "mcqs": [
                    {
                        "question": f"What is {topic}?",
                        "options": ["Concept", "Number", "Shape", "None"],
                        "answer": "Concept"
                    }
                ]
            }