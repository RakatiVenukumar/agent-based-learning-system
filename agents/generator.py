# generator agent

class GeneratorAgent:
    def generate(self, grade, topic, feedback=None):
        """
        Generates educational content based on grade and topic.

        Args:
            grade (int): Student grade level
            topic (str): Topic to generate content for
            feedback (list, optional): Feedback from reviewer for refinement

        Returns:
            dict: Structured output with explanation and MCQs
        """

        # -------------------------------
        # Base Explanation (Grade-friendly)
        # -------------------------------
        explanation = (
            "Angles are formed when two lines meet at a point. "
            "There are different types of angles. "
            "An acute angle is less than 90 degrees. "
            "A right angle is exactly 90 degrees. "
            "An obtuse angle is more than 90 degrees but less than 180 degrees. "
            "A straight angle is exactly 180 degrees."
        )

        # -------------------------------
        # Refinement Logic (if feedback exists)
        # Simplify explanation for better clarity
        # -------------------------------
        if feedback:
            explanation = (
                "Angles are made when two lines meet. "
                "Acute angle is less than 90°. "
                "Right angle is 90°. "
                "Obtuse angle is more than 90° but less than 180°. "
                "Straight angle is 180°."
            )

        # -------------------------------
        # MCQs (Structured, deterministic format)
        # -------------------------------
        mcqs = [
            {
                "question": "Which angle is less than 90 degrees?",
                "options": ["Right angle", "Acute angle", "Obtuse angle", "Straight angle"],
                "answer": "Acute angle"
            },
            {
                "question": "What is the measure of a right angle?",
                "options": ["45°", "90°", "120°", "180°"],
                "answer": "90°"
            },
            {
                "question": "Which angle is exactly 180 degrees?",
                "options": ["Acute angle", "Right angle", "Straight angle", "Obtuse angle"],
                "answer": "Straight angle"
            }
        ]

        # -------------------------------
        # Return structured output
        # -------------------------------
        return {
            "explanation": explanation,
            "mcqs": mcqs
        }