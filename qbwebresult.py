from flask import Flask, render_template
from qbpull import QBadapter

app = Flask(__name__)

@app.route("/")
def index():
    return "Test successful"

@app.route("/report")
def report():
    return 'Error. Please Call with path of survey index (e.g. "/report/1394")'

@app.route("/report/<survey_index>")
def mpc_result(survey_index):
    qba = QBadapter()
    latest_result = qba.get_latest_result(survey_index)
    testvar = latest_result["datetime"]
    questions = get_questions(latest_result)
    return render_template("report.html", testvar=testvar, data=latest_result, questions=questions)

def get_questions(full_result):
    questions = []
    for key in full_result:
        if key.startswith("v_"):
            questions.append(key)

    questions_sorted = sorted(questions, key=lambda x: int(x.split("_")[1]))
    return questions_sorted


if __name__ == "__main__":
    app.run()