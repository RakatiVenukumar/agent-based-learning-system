from flask import Flask, render_template, request
from agents.generator import GeneratorAgent
from agents.reviewer import ReviewerAgent

app = Flask(__name__)

# -----------------------------------
# Pipeline Function (same as before)
# -----------------------------------
def run_pipeline(grade, topic):
    generator = GeneratorAgent()
    reviewer = ReviewerAgent()

    initial_output = generator.generate(grade, topic)
    review = reviewer.review(initial_output, grade)

    refined_output = None

    if review["status"] == "fail":
        refined_output = generator.generate(
            grade,
            topic,
            feedback=review["feedback"]
        )

    return {
        "initial_output": initial_output,
        "review": review,
        "refined_output": refined_output
    }


# -----------------------------------
# Flask Route
# -----------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        grade = int(request.form["grade"])
        topic = request.form["topic"]

        result = run_pipeline(grade, topic)

    return render_template("index.html", result=result)


# -----------------------------------
# Run App
# -----------------------------------
if __name__ == "__main__":
    app.run(debug=True)