import tkinter as tk
from tkinter import messagebox

class QuizApp:
    # def __init__(self, master):
    #     self.master = master
    #     self.master.title("Quiz App")

    #     # Initialize variables
    #     self.user_choice = tk.IntVar(value=1)
    #     self.correct_answers = 0
    #     self.questions_answers = {
    #         "Q1": "A1", "Q2": "A2", "Q3": "A3", "Q4": "A4", "Q5": "A5",
    #         "Q6": "A6", "Q7": "A7", "Q8": "A8", "Q9": "A9", "Q10": "A10"
    #     }
    #     self.user_answers = {}

    #     # First screen setup
    #     self.setup_first_screen()

    def __init__(self, master):
        self.master = master
        self.master.title("Quiz App")

        # Initialize variables
        self.user_choice = tk.IntVar(value=1)
        self.correct_answers = 0
        self.current_question_index = 0

        # Questions and answers (You can replace these texts without changing the logic)
        self.questions = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10"]
        self.options = {
            "Q1": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "Q2": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "Q3": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "Q4": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "Q5": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "Q6": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "Q7": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "Q8": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "Q9": ["Option 1", "Option 2", "Option 3", "Option 4"],
            "Q10": ["Option 1", "Option 2", "Option 3", "Option 4"],
            # Add options for other questions
        }

        # Correct answers mapping (Q1: "Option 1", ...)
        self.correct_answers_map = {
            "Q1": "Option 1",
            "Q2": "Option 1",
            "Q3": "Option 1",
            "Q4": "Option 1",
            "Q5": "Option 1",
            "Q6": "Option 1",
            "Q7": "Option 1",
            "Q8": "Option 1",
            "Q9": "Option 1",
            "Q10": "Option 1",
            # Map other questions to their correct options
        }

        self.setup_first_screen()

    def calculate_score(self, choice, correct_answers):
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

    def setup_first_screen(self):
        # Add radio buttons for 1 to 5
        tk.Label(self.master, text="How likely are you to recommend our quiz? (1-5)").pack()
        for i in range(1, 6):
            tk.Radiobutton(self.master, text=str(i), variable=self.user_choice, value=i).pack()

        # Add a 'Next' button to go to the first question
        tk.Button(self.master, text="Next", command=self.next_question).pack()

    def next_question(self):
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            self.setup_question_screen(question)
            self.current_question_index += 1
        else:
            self.calculate_and_display_score()

    def setup_question_screen(self, question):
        # Clear the current screen
        for widget in self.master.winfo_children():
            widget.destroy()

        # Add the current question and its options
        tk.Label(self.master, text=question).pack()
        user_answer = tk.StringVar(value="None")

        for option in self.options[question]:
            tk.Radiobutton(self.master, text=option, variable=user_answer, value=option).pack()

        # Check the answer when moving to the next question
        tk.Button(self.master, text="Next Question", command=lambda: self.check_answer(question, user_answer.get())).pack()

    def check_answer(self, question, selected_option):
        if selected_option == self.correct_answers_map[question]:
            self.correct_answers += 1
        self.next_question()

    def calculate_and_display_score(self):
        # Clear the current screen
        for widget in self.master.winfo_children():
            widget.destroy()

        # Calculate the score
        score = self.calculate_score(self.user_choice.get(), self.correct_answers)

        # Display the score
        tk.Label(self.master, text=f"Your score is: {score}").pack()

def main():
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

