# Application to manage quiz webapp
# Name: Jorryn Skye Orias
# Date: Nov. 18, 2026

import json
import os
import random
import time
import uuid
from datetime import datetime, timedelta

from flask import Flask, jsonify, redirect, render_template, request, session, url_for

BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
QUESTION_FILE = os.path.join(BASE_FOLDER, "questions.json")
SCORE_FILE = os.path.join(BASE_FOLDER, "scores.json")
NUM_QUESTIONS_PER_QUIZ = 5
MAX_NAME_LENGTH = 30

# Global variables describe the quiz being played right now. Who is playing is
# remembered in quiz_owner so another visitor cannot use somebody else's quiz.

score = 0
question_number = 0
questions = []          # this quiz's questions, already chosen and shuffled
max_questions = 0
category = ""
quiz_owner = None       # user id of the player
start_time = 0
end_time = 0
last_result = None      # what happened on the question that was just answered
score_saved = False     # so reloading the result page cannot save the score twice

app = Flask(__name__)
# The secret key signs the session cookie. On a real server set QUIZ_SECRET_KEY instead.
app.secret_key = os.environ.get("QUIZ_SECRET_KEY", "change-this-secret-key")
app.permanent_session_lifetime = timedelta(days=365)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024   # the forms here are tiny, so refuse big requests


class QuestionFileError(Exception):
    """questions.json is missing, damaged or in the wrong format."""

# Quiz functions (from Assignment 1)

def check_questions(data):
    """Check the structure of questions.json so a bad edit gives a clear message instead of
    a crash in the middle of a quiz.

    Expected: {"Category": {"Question?": {"answers": ["correct", "wrong", ...],
                                          "explanation": "optional"}}}
    The FIRST answer is the correct one (the same rule as Assignment 1)."""
    if not isinstance(data, dict) or not data:
        raise QuestionFileError("The questions file must contain at least one category.")
    for category_name, category_questions in data.items():
        if not isinstance(category_questions, dict) or not category_questions:
            raise QuestionFileError(f"The category '{category_name}' must contain at least one question.")
        for question, details in category_questions.items():
            answers = details.get("answers") if isinstance(details, dict) else None
            good = (isinstance(answers, list) and len(answers) >= 2
                    and all(isinstance(a, str) and a.strip() for a in answers)
                    and len(set(answers)) == len(answers))
            if not good:
                raise QuestionFileError(
                    f"The question '{question}' needs at least two different, non-empty answers.")
            if not isinstance(details.get("explanation", ""), str):
                raise QuestionFileError(f"The explanation for '{question}' must be text.")


def load_questions():
    """Read questions.json (every time, so edits show up without a restart) and check it."""
    name = os.path.basename(QUESTION_FILE)
    try:
        question_file = open(QUESTION_FILE, "rb")
        raw = question_file.read()
        question_file.close()       # closed before decoding, so a bad file is never left open
        data = json.loads(raw.decode("utf-8"))
    except FileNotFoundError:
        raise QuestionFileError(f"The questions file '{name}' could not be found.") from None
    except json.JSONDecodeError as error:
        raise QuestionFileError(f"The questions file '{name}' is not valid JSON (near line {error.lineno}).") from None
    except (OSError, ValueError):
        raise QuestionFileError(f"The questions file '{name}' could not be read.") from None
    check_questions(data)
    return data


def prepare_questions(category_questions, num_questions):
    """Pick random questions and shuffle each question's answers (Assignment 1's
    prepare_questions plus the answer shuffle from ask_question).

    The correct answer is read BEFORE shuffling and kept as text, so the shuffled order
    never affects grading."""
    num_questions = min(num_questions, len(category_questions))
    chosen = random.sample(list(category_questions.items()), k=num_questions)
    prepared = []
    for question, details in chosen:
        answers = details["answers"]
        prepared.append({
            "question": question,
            "correct": answers[0],
            "options": random.sample(answers, k=len(answers)),
            "explanation": details.get("explanation", ""),
        })
    return prepared


def setup_quiz(chosen_category, category_questions):
    """Reset the global variables for a new quiz."""
    global score, question_number, questions, max_questions, category
    global quiz_owner, start_time, end_time, last_result, score_saved
    score = 0
    question_number = 0
    questions = prepare_questions(category_questions, NUM_QUESTIONS_PER_QUIZ)
    max_questions = len(questions)
    category = chosen_category
    quiz_owner = session.get("user_id")
    start_time = time.time()
    end_time = 0
    last_result = None
    score_saved = False


def quiz_is_active():
    """True when there is a quiz and it belongs to the visitor making this request."""
    return max_questions > 0 and quiz_owner is not None and quiz_owner == session.get("user_id")


def format_duration(seconds):
    """45 -> '45s', 125 -> '2m 05s'."""
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds}s"
    return f"{seconds // 60}m {seconds % 60:02d}s"


app.add_template_filter(format_duration, "duration")


def feedback_message(percent):
    """A short message for the result page."""
    if percent == 100:
        return "Perfect score! Excellent work."
    if percent >= 80:
        return "Great job! You know this topic well."
    if percent >= 60:
        return "Good effort. A little more practice and you will have it."
    return "Keep practicing. Review the questions below and try again."

# Visitors and score history (requirement 1). The cookie holds only a random id; the name
# and the history are kept in scores.json:
#   {"users": {"<id>": {"name": "Jorryn", "KPOP": [{"date", "category", "score", "total", "seconds"}]}}}

def validate_name(name):
    """Return the cleaned name or raise ValueError with a message for the visitor."""
    name = (name or "").strip()
    if not name:
        raise ValueError("Please enter your name.")
    if len(name) > MAX_NAME_LENGTH:
        raise ValueError(f"Your name must be {MAX_NAME_LENGTH} characters or fewer.")
    if not all(ch.isalnum() or ch in " -'_." for ch in name):
        raise ValueError("Your name can only contain letters, numbers, spaces and - ' _ .")
    if not any(ch.isalnum() for ch in name):
        raise ValueError("Your name must contain at least one letter or number.")
    return name


def load_scores():
    """Read scores.json. A missing file means no users yet. A damaged file is renamed (so
    nothing is lost) and the app starts again with an empty file."""
    try:
        score_file = open(SCORE_FILE, "rb")
        raw = score_file.read()
        score_file.close()
        data = json.loads(raw.decode("utf-8"))
    except FileNotFoundError:
        return {"users": {}}
    except ValueError:
        os.replace(SCORE_FILE, SCORE_FILE + ".damaged")
        return {"users": {}}
    if not isinstance(data, dict) or not isinstance(data.get("users"), dict):
        os.replace(SCORE_FILE, SCORE_FILE + ".damaged")
        return {"users": {}}
    return data


def save_scores(data):
    """Write to a temporary file, then swap it in, so a crash can never leave a half-written file."""
    temporary = SCORE_FILE + ".tmp"
    score_file = open(temporary, "w", encoding="utf-8")
    json.dump(data, score_file, indent=4)     # same call as Assignment 1's save_scores
    score_file.close()
    os.replace(temporary, SCORE_FILE)


def get_user():
    """The visitor named by the session cookie, or None for a new visitor."""
    user_id = session.get("user_id")
    if not user_id:
        return None
    return load_scores()["users"].get(user_id)


def is_whole_number(value):
    """True for 3, False for 3.5, '3' and True."""
    return isinstance(value, int) and not isinstance(value, bool)


def add_score(user_id, chosen_category, points, total, seconds):
    """Add a finished quiz to a user's history. Raises ValueError for impossible numbers
    and KeyError for an unknown user."""
    if not (is_whole_number(points) and is_whole_number(total)) or total < 1 or not 0 <= points <= total:
        raise ValueError("The score must be a whole number from 0 up to the number of questions.")
    if isinstance(seconds, bool) or not isinstance(seconds, (int, float)) or seconds < 0:
        raise ValueError("The time taken must be zero or more seconds.")
    entry = {"date": datetime.now().strftime("%Y-%m-%d %H:%M"), "category": chosen_category,
             "score": points, "total": total, "seconds": round(seconds)}
    data = load_scores()
    if user_id not in data["users"]:
        raise KeyError("Unknown user.")
    data["users"][user_id]["history"].append(entry)
    save_scores(data)
    return entry


def show_welcome_page(error=None, name_value="", status=200):
    """The index page: a name form for a new visitor, or the category menu and score history
    for a returning one."""
    user = get_user()
    history = list(reversed(user["history"])) if user else []
    page = render_template("index.html", user=user, history=history,
                           categories=list(load_questions().keys()), error=error,
                           name_value=name_value, just_registered=session.pop("just_registered", False))
    return page, status

# Pages

@app.route('/')
def index():
    return show_welcome_page()


@app.route('/register', methods=['POST'])
def register():
    """Save a first-time visitor's name and remember them with a cookie."""
    name = request.form.get("name", "")
    try:
        name = validate_name(name)
    except ValueError as error:
        return show_welcome_page(error=str(error), name_value=name.strip()[:MAX_NAME_LENGTH], status=400)
    user_id = uuid.uuid4().hex
    data = load_scores()
    data["users"][user_id] = {"name": name, "history": []}
    save_scores(data)
    session.permanent = True        # keep the cookie after the browser is closed
    session["user_id"] = user_id
    session["just_registered"] = True
    return redirect(url_for('index'))


@app.route('/switch-user', methods=['POST'])
def switch_user():
    """'Not you?' forgets the visitor in this browser. Their saved history stays in the file."""
    session.clear()
    return redirect(url_for('index'))


@app.route('/start', methods=['POST'])
def start():
    """Set up a quiz in the chosen category."""
    if get_user() is None:
        return redirect(url_for('index'))
    all_questions = load_questions()
    chosen = request.form.get("category", "")
    if chosen not in all_questions:
        return show_welcome_page(error="Please choose one of the listed categories.", status=400)
    setup_quiz(chosen, all_questions[chosen])
    return redirect(url_for('quiz'))


def show_question(error=None, status=200):
    page = render_template('quiz.html', question=questions[question_number]['question'],
                           question_number=question_number, max_questions=max_questions,
                           options=questions[question_number]['options'], category=category,
                           error=error)
    return page, status


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    global score, question_number, last_result
    if not quiz_is_active():
        return redirect(url_for('index'))
    if question_number >= max_questions:
        return redirect(url_for('result')) # the quiz is over

    if request.method == 'POST':

        # The form carries the number of the question it was shown for. If that is not the
        # current question (a double click, or the Back button), do not score anything.

        if request.form.get("question_number") != str(question_number):
            return redirect(url_for('quiz'))
        answer = request.form.get('answer')
        if answer is None:
            return show_question("Please choose an answer before submitting.", 400)
        current = questions[question_number]
        if answer not in current['options']:
            return show_question("Please choose one of the answers shown.", 400)

        current['chosen'] = answer      # kept so the result page can list the missed questions
        correct = (answer == current['correct'])
        if correct:
            score += 1
        last_result = {"question": current['question'], "options": current['options'],
                       "chosen": answer, "correct_answer": current['correct'],
                       "was_correct": correct, "explanation": current['explanation']}
        question_number += 1
        return redirect(url_for('question_result'))  # redirect so a refresh does not re-submit

    return show_question()


@app.route('/question_result')
def question_result():
    """Feedback for the question just answered (requirement 7)."""
    if not quiz_is_active() or last_result is None or question_number == 0:
        return redirect(url_for('quiz'))
    return render_template('question_result.html', result=last_result, score=score,
                           question_number=question_number, max_questions=max_questions,
                           is_last=question_number >= max_questions)


@app.route('/result')
def result():
    """Final score, correct/incorrect counts, time taken and the questions to review. The score
    is saved to the visitor's history only once, even if this page is reloaded."""
    global end_time, score_saved
    if not quiz_is_active():
        return redirect(url_for('index'))
    if question_number < max_questions:
        return redirect(url_for('quiz'))

    if end_time == 0:
        end_time = time.time()      # fixed once, so reloading does not change the time taken
    seconds = round(end_time - start_time)
    save_failed = False
    if not score_saved:
        try:
            add_score(quiz_owner, category, score, max_questions, seconds)
            score_saved = True
        except (OSError, KeyError):
            save_failed = True      # still show the result, and say it was not saved
    percent = round(100 * score / max_questions)
    return render_template('result.html', score=score, max_questions=max_questions,
                           incorrect=max_questions - score, percent=percent, seconds=seconds,
                           category=category, message=feedback_message(percent),
                           save_failed=save_failed, missed=missed_questions())


def missed_questions():
    """The questions the player got wrong, for 'areas for improvement'."""
    return [q for q in questions if q.get("chosen") is not None and q["chosen"] != q["correct"]]

# REST API

def api_error(message, status):
    return jsonify({"error": message}), status


@app.route('/api/categories')
def api_categories():
    return jsonify({"categories": list(load_questions().keys())})


@app.route('/api/questions')
def api_questions():
    """Randomized questions for a category. The correct answers are never sent."""
    all_questions = load_questions()
    chosen = request.args.get("category", "")
    if chosen not in all_questions:
        return api_error(f"Unknown category '{chosen}'. Use /api/categories to see the choices.", 404)
    count = request.args.get("count", str(NUM_QUESTIONS_PER_QUIZ))
    if not count.isdigit() or not 1 <= int(count) <= 50:
        return api_error("count must be a whole number from 1 to 50.", 400)
    prepared = prepare_questions(all_questions[chosen], int(count))
    return jsonify({"category": chosen,
                    "questions": [{"question": q["question"], "options": q["options"]} for q in prepared]})


@app.route('/api/scores', methods=['GET'])
def api_get_scores():
    user = get_user()
    if user is None:
        return api_error("No user is registered in this browser session.", 401)
    return jsonify({"name": user["name"], "history": list(reversed(user["history"]))})


@app.route('/api/scores', methods=['POST'])
def api_add_score():
    user = get_user()
    if user is None:
        return api_error("No user is registered in this browser session.", 401)
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return api_error("Send a JSON object with category, score, total and seconds.", 400)
    if data.get("category") not in load_questions():
        return api_error("category must be one of the quiz categories.", 400)
    try:
        entry = add_score(session["user_id"], data["category"], data.get("score"),
                          data.get("total"), data.get("seconds", 0))
    except ValueError as error:
        return api_error(str(error), 400)
    return jsonify(entry), 201

# Friendly error pages

def show_error(title, message, status):
    if request.path.startswith("/api/"):
        return api_error(message, status)
    return render_template("error.html", title=title, message=message), status


@app.errorhandler(QuestionFileError)
def handle_question_file_error(error):
    return show_error("The quiz could not be loaded", str(error), 500)


@app.errorhandler(OSError)
def handle_file_error(error):
    return show_error("Something went wrong", "The data file could not be read or saved. Please try again.", 500)


@app.errorhandler(404)
def handle_not_found(error):
    return show_error("Page not found", "That page does not exist.", 404)


@app.errorhandler(405)
def handle_wrong_method(error):
    return show_error("Not allowed", "That action is not allowed here.", 405)


@app.errorhandler(413)
def handle_too_large(error):
    return show_error("Too large", "That request was too large.", 413)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()