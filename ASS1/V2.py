# Interactive quiz system, second version 
# Make a list with the questions and correct answers 

questions = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What is the capital of Germany?", "answer": "Berlin"},
    {"question": "The Last Supper was painted by which artist?", "answer": "Leonardo da Vinci"}
]

for question, correct_answer in questions:
    answer = input(f"{question} ")
    if answer == question['answer']:
        print("Correct!")
    else:
        print(f"The answer is '{question['answer']}' not {answer!r}.")
