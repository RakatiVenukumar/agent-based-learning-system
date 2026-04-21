from flask import Flask, render_template, request
from agents.generator import GeneratorAgent
from agents.reviewer import ReviewerAgent

app = Flask(__name__)


def run_pipeline(grade, topic):
    g = GeneratorAgent()
    r = ReviewerAgent()

    initial = g.generate(grade, topic)
    review = r.review(initial, grade)

    refined = None
    if review["status"] == "fail":
        refined = g.generate(grade, topic, review["feedback"])

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

        if not topic.strip() or not any(c.isalnum() for c in topic):
            error = "Invalid topic"

        elif grade <= 2 and any(word in topic.lower() for word in ["integration", "differentiation"]):
            error = "Topic too advanced for this grade"

        else:
            result = run_pipeline(grade, topic)

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True)