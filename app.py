from agents.generator import GeneratorAgent
from agents.reviewer import ReviewerAgent

# -----------------------------------
# Pipeline Function
# -----------------------------------
def run_pipeline(grade, topic):
    """
    Runs the full agent pipeline:
    1. Generate content
    2. Review content
    3. Refine once if failed

    Args:
        grade (int)
        topic (str)

    Returns:
        dict: Contains initial output, review, and refined output (if any)
    """

    generator = GeneratorAgent()
    reviewer = ReviewerAgent()

    # -------------------------------
    # Step 1: Generate content
    # -------------------------------
    initial_output = generator.generate(grade, topic)

    # -------------------------------
    # Step 2: Review content
    # -------------------------------
    review = reviewer.review(initial_output, grade)

    refined_output = None

    # -------------------------------
    # Step 3: Refinement (ONLY ONCE)
    # -------------------------------
    if review["status"] == "fail":
        refined_output = generator.generate(
            grade,
            topic,
            feedback=review["feedback"]
        )

    # -------------------------------
    # Final result
    # -------------------------------
    return {
        "initial_output": initial_output,
        "review": review,
        "refined_output": refined_output
    }


# -----------------------------------
# Temporary test run (for terminal)
# -----------------------------------
if __name__ == "__main__":
    result = run_pipeline(4, "Types of angles")

    import json
    print(json.dumps(result, indent=2))