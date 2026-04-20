class ReviewerAgent:
    def review(self, content, grade):
        feedback = []

        explanation = content.get("explanation", "")
        mcqs = content.get("mcqs", [])

        # Explanation checks
        word_count = len(explanation.split())

        if word_count < 15:
            feedback.append("Explanation too short")

        if word_count > 120:
            feedback.append("Explanation too long")

        if grade <= 4 and word_count > 50:
            feedback.append("Too complex for lower grade")

        if grade >= 8 and word_count < 20:
            feedback.append("Too simple for higher grade")

        # MCQ count
        if len(mcqs) != 3:
            feedback.append("Must have exactly 3 MCQs")

        questions_seen = set()

        for i, mcq in enumerate(mcqs):
            q = mcq.get("question", "")
            options = mcq.get("options", [])
            answer = mcq.get("answer")

            if not q:
                feedback.append(f"Q{i+1} missing question")

            if q in questions_seen:
                feedback.append(f"Q{i+1} duplicate question")
            questions_seen.add(q)

            if len(options) != 4:
                feedback.append(f"Q{i+1} must have 4 options")

            if answer not in options:
                feedback.append(f"Q{i+1} answer not in options")

        status = "pass" if not feedback else "fail"

        return {
            "status": status,
            "feedback": feedback
        }