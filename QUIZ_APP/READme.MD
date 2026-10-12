Quiz App – Design Document

Name: Jorryn Skye Orias 
Assignment: Assignment 1 – Quiz App 

This quiz app implements additional requirement #1 (the history of scores is written to a file) and requirement #10 (a 50/50 lifeline that can be used once per game). It also includes the extra credit (user login, a high score for each user, and a grand champion). To run it, keep quiz.py and questions.json in the same folder and run python quiz.py. The file scores.json is created automatically the first time the quiz is played.

Data Structure Justification

The questions are stored in questions.json as a dictionary of dictionaries. The top-level keys are categories, and each category maps a question to a dictionary that holds an "answers" list. The correct answer is always the first item in the list, but is randomized when the user actually does the quiz. 

I chose this design mainly so that the questions are easy for a person to read and edit. Adding a question only means typing the question and its answers with the right one first, so there is no separate "correct answer" field or index number that could end up pointing at the wrong item if someone deletes or reorders an answer.

Function Design

The two most important non-trivial functions are get_answer() and apply_fifty_fifty(). The function get_answer() shows the labeled choices and keeps asking until it receives a valid answer, and it returns the chosen answer along with whether the 50/50 was used. I made it a separate function because it solves one specific problem, which turns the unpredictable keyboard input from the user (ex. if the student doesn't add the right function) into an answer the rest of the program can trust. This lets ask_question() assume it always receives a real answer and only worry about grading it, and it keeps every rule about input in one place so those rules can be changed without touching the scoring.

The function apply_fifty_fifty() removes half of the answers (two out of four) and only ever chooses from the wrong ones, so the correct answer can never be eliminated. The remaining answers keep their original letters, so if "c" and "d" are left the player still sees "c" and "d" and does not have to re-read the list to find where an answer moved.

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
 
 Control Flow

Every place where the program takes input uses a validation loop that keeps asking until the input is acceptable. For answering a question the loop looks like this:

python
while True:
    choice = input("Choice? ").strip().lower()
    if choice in labeled_answers:
        return labeled_answers[choice]
    ...
    else:
        print(f"Invalid choice. Please select one of {', '.join(labeled_answers.keys())}.")

If the player types something that is not a valid letter, such as q, a number, or just pressing Enter, the input is ignored, the valid letters are shown, and the same question is asked again. The question is never skipped or counted as wrong because of a typo.

I chose a loop that only exits when the input is valid because it keeps the quiz fair and the program stable. A typo can never cost the player a point, so the final score reflects real answers, and bad input can never reach the grading code or crash the program.

Use of AI 

For this assignment, I used claude as my AI tool . Using the code that we have for ASS 1, I used that code as the design and foundation of the rest of my code for the quiz while I also asked claude questions and following suggestions that claude provided while working on the assignment.