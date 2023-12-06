import tkinter as tk
from tkinter import messagebox
import json
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import make_interp_spline, interp1d

class QuizApp:
    def center_window(self):
        window_width = 1020
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

        # Create a title label above the grid
        title_label = tk.Label(self.master, text="Choose a topic", font=('Helvetica', 32, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, sticky='nsew')

        # Set up a grid for subject selection buttons
        rows = 3  # Adjusted to include the title row
        cols = 3
        button_padx = 10
        button_pady = 10
        for i, subject in enumerate(self.subjects):
            btn = tk.Button(self.master, text=subject, command=lambda subj=subject: self.subject_selected(subj), font=('Helvetica', 24))
            # Place buttons in grid starting from the second row to leave space for the title
            btn.grid(row=(i // cols) + 1, column=i % cols, sticky='nsew', padx=button_padx, pady=button_pady)

        # Configure grid rows and columns to expand equally
        for i in range(rows):
            self.master.grid_rowconfigure(i, weight=1)
        for i in range(cols):
            self.master.grid_columnconfigure(i, weight=1)

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

        # Bind the close event to the close function
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

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

    def on_close(self):
        """Handler function to call when the window is closed."""
        plt.close('all')  # Close all matplotlib plots
        self.master.quit()  # Quit the Tkinter main loop
        self.master.destroy()  # Destroy the Tkinter window

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

        # Create a frame for the radio buttons and labels
        frame = tk.Frame(self.master)
        frame.pack(expand=True)

        # Add radio buttons for 1 to 5
        tk.Label(frame, text="How confident are you in this subject?").pack()
        tk.Label(frame, text="(1 = I know nothing - 5 = I'm an expert)").pack()
        for i in range(1, 6):
            tk.Radiobutton(frame, text=str(i), variable=self.user_choice, value=i).pack()

        # Add a 'Next' button to go to the first question
        tk.Button(frame, text="Next", command=self.next_question).pack()

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

        # Create a frame for the radio buttons
        frame = tk.Frame(self.master)
        frame.pack(expand=True)

        # Add the current question
        tk.Label(frame, text=question).pack()

        # Radio buttons aligned to the left
        user_answer = tk.StringVar(value="None")
        for option in self.options[question]:
            tk.Radiobutton(frame, text=option, variable=user_answer, value=option, anchor='w').pack(fill='x')

        # Next Question button
        tk.Button(frame, text="Next Question", command=lambda: self.check_answer(question, user_answer.get())).pack()

    def check_answer(self, question, selected_option):
        if selected_option == self.correct_answers_map[question]:
            self.correct_answers += 1
        self.next_question()

    def plot_score_on_curve(self, score):
        # Normalize the score to be between 0 and 1
        normalized_score = score / 100

        # Load dkecurve.json file for point data
        with open('dkecurve.json') as json_file:
            json_data = json.load(json_file)

        x_values = json_data['x']
        y_values = json_data['y']

        # Create a spline interpolation of the data
        x_new = np.linspace(min(x_values), max(x_values), 300)  # More points for a smoother curve
        spl = interp1d(x_values, y_values, kind='cubic')

        # Normalize the score to the X values range
        min_x, max_x = min(x_values), max(x_values)
        normalized_score = min_x + (max_x - min_x) * normalized_score

        # Use the spline function to find the corresponding Y value
        user_y = spl(normalized_score)

        # Create a new figure and axis
        fig, ax = plt.subplots()

        # Plotting the smooth curve on the axis
        ax.plot(x_new, spl(x_new))
        # Mark the user's position on the axis
        ax.plot(normalized_score, user_y, 'ro')  # 'ro' for red dot

        # Annotate the user's score on the axis
        ax.annotate(f"You are here!", (normalized_score, user_y), textcoords="offset points", xytext=(0,10), ha='center')

        # Adding annotations directly on the axis
        ax.text(20, 4, "Peak of Mount Stupid", horizontalalignment='center', verticalalignment='bottom')
        ax.text(27, 1.6, "Valley of Despair", horizontalalignment='center', verticalalignment='top')
        ax.text(55, 2, "Slope of Enlightenment", horizontalalignment='center', verticalalignment='bottom')
        ax.text(88, 4, "Plateau of Sustainability", horizontalalignment='center', verticalalignment='bottom')

        # Add labels and title to the axis
        ax.set_title("Your Position on the Dunning-Kruger Effect Curve")
        ax.set_xlabel("Knowledge - Experience")
        ax.set_ylabel("Confidence")
        ax.grid(True)

        # Embedding the figure in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.master)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def calculate_and_display_score(self):
        # Clear the current screen
        for widget in self.master.winfo_children():
            widget.destroy()

        # Calculate the score
        score = self.calculate_score(self.user_choice.get(), self.correct_answers)

        # Display the score
        # debug log the score variable and its type
        print(score)
        self.plot_score_on_curve(score)

def main():
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

