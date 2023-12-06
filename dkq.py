def calculate_score(choice, correct_answers):
    if choice in [1, 2]:
        if correct_answers > 3:
            return 40 + (correct_answers - 4) * 4  # Ensures score is within 40-60
        else:
            return correct_answers  # Ensures score is within 1-10

    elif choice == 3:
        if correct_answers < 2:
            return correct_answers
        elif correct_answers < 8:
            return 41 + (correct_answers - 2) * 6  # Avoids 20-40 range
        else:
            return 89 + correct_answers  # Ensures high scores for good performance

    elif choice in [4, 5]:
        if correct_answers < 5:
            return 20 + correct_answers * 4  # Ensures score is within 20-40
        else:
            return 60 + (correct_answers - 5) * 8  # Ensures score is within 60-100

def main():
    user_choice = int(input("Enter a number from 1 to 5: "))
    correct_answers = 0

    # Example questions (you can replace these with your actual questions)
    questions = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10"]
    answers = ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10"]

    for i in range(len(questions)):
        user_answer = input(questions[i] + ": ")
        if user_answer == answers[i]:
            correct_answers += 1

    score = calculate_score(user_choice, correct_answers)
    print(f"Your score is: {score}")

if __name__ == "__main__":
    main()
