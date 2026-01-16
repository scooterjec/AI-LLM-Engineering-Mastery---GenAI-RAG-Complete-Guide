questions = {
    "Capital of France ": "Paris",
    "2 + 2 ":"4"
}

score = 0
total_q = len(questions)
print("Welcome!!")
print("Type 'quit' to exit\n")
for q,r in questions.items():
    user_answer = input(q + "")
    if user_answer.lower() == 'quit':
        break
    elif user_answer.lower() == r.lower():
        print("Correct!!")
        score +=1
    else:
        print(f"Error! Corresct answer is: {r}")
    print(user_answer)
print(f"Your score is {score}/{total_q}")
    