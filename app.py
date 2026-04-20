from flask import Flask, render_template, request
from agents.generator import GeneratorAgent
from agents.reviewer import ReviewerAgent

app = Flask(__name__)


def run_pipeline(grade, topic):
    generator = GeneratorAgent()
    reviewer = ReviewerAgent()

    initial = generator.generate(grade, topic)
    review = reviewer.review(initial, grade)

    refined = None
    if review["status"] == "fail":
        refined = generator.generate(grade, topic, review["feedback"])

    return {
        "initial_output": initial,
        "review": review,
        "refined_output": refined
    }


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        topic = request.form["topic"]
        grade = int(request.form["grade"])

        if not topic.strip():
            error = "Topic cannot be empty"
        else:
            result = run_pipeline(grade, topic)

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True)