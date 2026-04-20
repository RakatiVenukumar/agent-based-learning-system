# reviewer agent

class ReviewerAgent:
    def review(self, content, grade):
        """
        Reviews the generated educational content.

        Args:
            content (dict): Output from GeneratorAgent
            grade (int): Target grade level

        Returns:
            dict: Review result with status and feedback
        """

        feedback = []

        explanation = content.get("explanation", "")
        mcqs = content.get("mcqs", [])

        # -------------------------------
        # 1. Check Explanation Length (Clarity)
        # Too long → not suitable for lower grades
        # -------------------------------
        word_count = len(explanation.split())
        if grade <= 4 and word_count > 60:
            feedback.append("Explanation is too long for Grade 4")

        # -------------------------------
        # 2. Check Concept Coverage (Correctness)
        # Ensure key concept (straight angle = 180°) exists
        # -------------------------------
        if "180" not in explanation:
            feedback.append("Missing explanation of straight angle (180 degrees)")

        # -------------------------------
        # 3. Check MCQ Relevance
        # Questions should match topic (angles)
        # -------------------------------
        for i, mcq in enumerate(mcqs):
            if "angle" not in mcq["question"].lower():
                feedback.append(f"Question {i+1} may not relate to angles")

        # -------------------------------
        # 4. Check MCQ Structure (Safety check)
        # -------------------------------
        for i, mcq in enumerate(mcqs):
            if len(mcq.get("options", [])) != 4:
                feedback.append(f"Question {i+1} does not have 4 options")

        # -------------------------------
        # Final Status
        # -------------------------------
        status = "pass" if len(feedback) == 0 else "fail"

        return {
            "status": status,
            "feedback": feedback
        }