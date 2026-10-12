# Interactive quiz system, final version
# Name: Jorryn Skye Orias
# Date: Oct 11th, 2026

#   Features
#   Requirement 1  - Score history is written to a file (scores.json)
#   Requirement 10 - 50/50 lifeline, usable once per game

#   Files used:
#   questions.json - the quiz questions, grouped by category
#   scores.json    - users, their high scores and their score history
#                    (created automatically the first time the quiz is run)
#   Only random, string and json are imported (the same as the class examples).
 
from string import ascii_lowercase
import random
import json
 
QUESTION_FILE = "questions.json"
SCORE_FILE = "scores.json"
NUM_QUESTIONS_PER_QUIZ = 5
FIFTY_FIFTY_COMMAND = "50"
 
 

# Score file (File I/O is allowed for the score history)

 
def load_scores():
    """Return the saved user data. If scores.json does not exist yet (or is
    empty) return a fresh, empty structure."""
    # Opening in "a" (append) mode creates the file if it is missing and
    # never erases anything, so reading it afterwards is always safe.
    score_file = open(SCORE_FILE, "a")
    score_file.close()
 
    score_file = open(SCORE_FILE, "r")
    text = score_file.read()
    score_file.close()
 
    if text == "":
        return {"users": {}}
    return json.loads(text)
 
 
def save_scores(data):
    """Write all user data (passwords, high scores, history) to the file."""
    score_file = open(SCORE_FILE, "w")
    json.dump(data, score_file, indent=4)
    score_file.close()
 
 

# Users, login, and scores

 
def login(data):
    """Ask for a username and password. A new username creates an account;
    an existing one must give the right password. Re-prompts until the login
    succeeds. Returns the username."""
    users = data["users"]
 
    while not (username := input("Username: ").strip().lower()):
        print("Username cannot be empty.")
 
    if username in users:
        while input("Password: ") != users[username]["password"]:
            print("Incorrect password. Try again.")
        print(f"Welcome back, {username}!")
    else:
        print(f"New user '{username}'. Creating your account.")
        while not (password := input("Choose a password: ")):
            print("Password cannot be empty.")
        # NOTE: stored as plain text because encryption packages have not
        # been covered. A real application should hash passwords.
        users[username] = {"password": password, "high_score": 0, "history": []}
        print(f"Welcome, {username}!")
 
    return username
 
 
def get_grand_champion(users):
    """Return (name, score) of the user with the highest high score.
    The name is None if nobody has scored yet."""
    champion = None
    best_score = 0
    for name, info in users.items():
        if info["high_score"] > best_score:
            champion = name
            best_score = info["high_score"]
    return champion, best_score
 
 
def record_score(data, username, category, score, total):
    """Add this game to the user's history, announce a new personal high
    score or a new grand champion, then save everything to the file."""
    users = data["users"]
    user = users[username]
 
    # Find the champion BEFORE updating this user's score
    champion, champion_score = get_grand_champion(users)
 
    user["history"].append({"category": category, "score": score, "total": total})
 
    if score > user["high_score"]:
        user["high_score"] = score
        print(f"*** NEW HIGH SCORE for {username}: {score}! ***")
 
    if score > champion_score:
        if champion == username:
            print("*** You extended your lead as GRAND CHAMPION! ***")
        else:
            print("*** You are the new GRAND CHAMPION! ***")
 
    save_scores(data)
 
    champion, champion_score = get_grand_champion(users)
    if champion:
        print(f"Grand champion: {champion} with {champion_score}")
 
 

# Questions

 
def choose_category(questions):
    """Show the categories and return the one the user picks.
    Re-prompts until the choice is valid."""
    labeled_categories = dict(zip(ascii_lowercase, questions.keys()))
 
    print("\nChoose a category:")
    for label, category in labeled_categories.items():
        print(f"{label}. {category}")
 
    while (choice := input("Category? ").strip().lower()) not in labeled_categories:
        print(f"Invalid choice. Please select one of {', '.join(labeled_categories.keys())}.")
 
    return labeled_categories[choice]
 
 
def prepare_questions(category_questions, num_questions):
    """Pick a random set of questions from one category. Each item is
    (question, details); details is a dictionary with an "answers" list
    (correct answer FIRST) and an optional "media" entry."""
    num_questions = min(num_questions, len(category_questions))
    return random.sample(list(category_questions.items()), k=num_questions)
 
 
def show_media(media):
    """Tell the user which image/video belongs to the question. (Opening it
    automatically would need a package that has not been covered.)"""
    if media:
        print(f"\nThis question has media. Open this file or link: {media}")
 
 

# 50/50 lifeline (Requirement 10)

 
def apply_fifty_fifty(labeled_answers, correct_answer):
    """Remove half of the answers (2 of 4), only ever removing WRONG ones.
 
    The remaining answers keep their original labels, so the letters on
    screen never shift while the user is thinking. Returns a new dictionary
    holding only the labels/answers that are still available."""

    wrong_labels = []
    for label, answer in labeled_answers.items():
        if answer != correct_answer:
            wrong_labels.append(label)
 
    removed = random.sample(wrong_labels, k=len(labeled_answers) // 2)
 
    remaining = {}
    for label, answer in labeled_answers.items():
        if label not in removed:
            remaining[label] = answer
    return remaining
 
 
def show_options(labeled_answers):
    """Print the answer choices."""
    for label, answer in labeled_answers.items():
        print(f"{label}. {answer}")
 
 
def get_answer(alternatives, correct_answer, fifty_fifty_available):
    """Show the choices and keep asking until the user gives a valid label.
    The user may also type the 50/50 command if the lifeline is available.
    Returns (chosen_answer, fifty_fifty_used_this_question)."""
    labeled_answers = dict(zip(ascii_lowercase, alternatives))
    used_now = False
 
    show_options(labeled_answers)
 
    while True:
        if fifty_fifty_available and not used_now:
            prompt = f"Choice (or '{FIFTY_FIFTY_COMMAND}' for to remove half of the wrong answers)? "
        else:
            prompt = "Choice? "
        choice = input(prompt).strip().lower()
 
        if choice in labeled_answers:
            return labeled_answers[choice], used_now
        elif choice == FIFTY_FIFTY_COMMAND and fifty_fifty_available and not used_now:
            if len(labeled_answers) < 3:
                # Removing half would leave only the right answer
                print("50/50 needs at least 3 answers. It was not used.")
            else:
                labeled_answers = apply_fifty_fifty(labeled_answers, correct_answer)
                used_now = True
                print("50/50 used! Two wrong answers have been removed:")
                show_options(labeled_answers)
        else:
            print(f"Invalid choice. Please select one of {', '.join(labeled_answers.keys())}.")
 
 
def ask_question(question, details, fifty_fifty_available):
    """Ask one question. Returns (points, fifty_fifty_used)."""
    correct_answer = details["answers"][0]
    ordered_alternatives = random.sample(details["answers"], k=len(details["answers"]))
 
    show_media(details.get("media"))
    answer, used = get_answer(ordered_alternatives, correct_answer, fifty_fifty_available)
 
    if answer == correct_answer:
        print("Correct!")
        return 1, used
    else:
        print(f"The answer is {correct_answer!r}, not {answer!r}.")
        return 0, used
 
 
def play_quiz(selected_questions):
    """Run one full game and return the number of correct answers.
    The 50/50 lifeline can be used only once for the whole game."""
    num_correct = 0
    fifty_fifty_available = True
 
    for num, (question, details) in enumerate(selected_questions, start=1):
        print(f"\nQuestion {num}: {question}")
        points, used = ask_question(question, details, fifty_fifty_available)
        num_correct += points
        if used:
            fifty_fifty_available = False
 
    return num_correct
 
 
# Main program logic starts here

question_file = open(QUESTION_FILE, "r")
questions = json.load(question_file)
question_file.close()
 
data = load_scores()
 
print("=== Welcome to the Quiz Game! ===")
username = login(data)
save_scores(data)  # saves a brand new account right away
 
playing = True
while playing:
    category = choose_category(questions)
    selected_questions = prepare_questions(questions[category], NUM_QUESTIONS_PER_QUIZ)
 
    score = play_quiz(selected_questions)
    total = len(selected_questions)
    print(f"\nYou got {score} out of {total} correct.")
 
    record_score(data, username, category, score, total)
 
    while (again := input("\nPlay again? (Y/N) ").strip().upper()) not in ("Y", "N"):
        print("Please enter Y or N.")
    if again == "N":
        print("Thanks for playing!")
        playing = False