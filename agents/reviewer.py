class ReviewerAgent:
    def review(self, content, grade):

        feedback = []

        explanation = content.get("explanation", "")
        mcqs = content.get("mcqs", [])

        words = len(explanation.split())

        # Grade mismatch
        if grade <= 3 and words > 40:
            feedback.append("Too complex for lower grade")

        if grade >= 8 and words < 20:
            feedback.append("Too simple for higher grade")

        if words > 120:
            feedback.append("Explanation too long")

        # MCQ checks
        if len(mcqs) != 3:
            feedback.append("Must have exactly 3 MCQs")

        seen = set()

        for i, mcq in enumerate(mcqs):
            q = mcq.get("question", "").lower()
            options = mcq.get("options", [])
            answer = mcq.get("answer")

            if not q:
                feedback.append(f"Q{i+1} missing question")

            if q in seen:
                feedback.append(f"Q{i+1} duplicate")
            seen.add(q)

            if len(options) != 4:
                feedback.append(f"Q{i+1} needs 4 options")

            if answer not in options:
                feedback.append(f"Q{i+1} answer not in options")

            if any(x in q for x in ["figure", "diagram", "image"]):
                feedback.append(f"Q{i+1} needs visual")

        return {
            "status": "pass" if not feedback else "fail",
            "feedback": feedback
        }