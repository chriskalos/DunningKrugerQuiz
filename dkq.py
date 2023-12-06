import tkinter as tk
from tkinter import messagebox
import json
import os

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz App")

        # Initialize variables
        self.user_choice = tk.IntVar(value=1)
        self.correct_answers = 0
        self.current_question_index = 0

        # Subjects and related data (placeholders for now)
        self.subjects = ["Photography", "Computer Science", "Nature", "Physics", "Mathematics", "Cooking"]
        
        # Call the method to set up the zeroth screen
        self.setup_zeroth_screen()

        # Center the window
        self.center_window()

    def center_window(self):
        window_width = 800
        window_height = 600

        # Get the screen dimension
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Find the center position
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # Set the window size and position
        self.master.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    def setup_zeroth_screen(self):
        # Clear the current screen
        for widget in self.master.winfo_children():
            widget.destroy()

        # Layout for subject selection buttons
        for subject in self.subjects:
            tk.Button(self.master, text=subject, command=lambda subj=subject: self.subject_selected(subj)).pack()

    def subject_selected(self, subject):
        # Convert subject name to filename
        filename = subject.replace(" ", "").lower() + '.json'
        
        # Check if file exists
        if not os.path.exists(filename):
            messagebox.showerror("Error", f"Quiz file for {subject} not found.")
            return

        # Load questions and answers from JSON file
        with open(filename, 'r') as file:
            data = json.load(file)
            self.questions = [q['question'] for q in data['questions']]
            self.options = {q['question']: q['options'] for q in data['questions']}
            self.correct_answers_map = {q['question']: q['correct_answer'] for q in data['questions']}

        # Call the first screen setup after a subject is selected
        self.setup_first_screen()

    def __init__(self, master):
        self.master = master
        self.master.title("Quiz App")

        # Initialize variables
        self.user_choice = tk.IntVar(value=1)
        self.correct_answers = 0
        self.current_question_index = 0

        # Initialize quiz data structures
        self.questions = []
        self.options = {}
        self.correct_answers_map = {}

        # Subjects and related data (placeholders for now)
        self.subjects = ["Photography", "Computer Science", "Nature", "Physics", "Mathematics", "Cooking"]

        # Call the method to set up the zeroth screen
        self.setup_zeroth_screen()

        # Center the window
        self.center_window()

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
       # Clear the current screen, if any
        for widget in self.master.winfo_children():
            widget.destroy() 
        
        # Add radio buttons for 1 to 5
        tk.Label(self.master, text="How confident are you in this subject?").pack()
        tk.Label(self.master, text="(1 = I know nothing - 5 = I'm an expert)").pack()
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

