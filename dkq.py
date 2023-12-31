import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import make_interp_spline, interp1d
import glob

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

        # Create a title label above the dropdown
        title_label = tk.Label(self.master, text="Choose a topic", font=('Helvetica', 32, 'bold'))
        title_label.pack(pady=(20, 10))  # Add some padding above and below the title

        # Find all JSON files and extract their names
        json_files = glob.glob('*.json')
        self.subjects_info = {}  # Dictionary to map friendly names to filenames

        for file in json_files:
            with open(file, 'r') as json_file:
                data = json.load(json_file)
                subject_name = data.get('name', 'Unknown')  # Default to 'Unknown' if no name is found
                self.subjects_info[subject_name] = file  # Map the friendly name to its filename

        # Create a combobox for subject selection with the friendly names
        self.subject_combobox = ttk.Combobox(self.master, values=list(self.subjects_info.keys()), font=('Helvetica', 24), state="readonly")
        self.subject_combobox.pack(pady=10)

        # Select button to confirm the choice
        select_button = tk.Button(self.master, text="Select", command=self.on_subject_select, font=('Helvetica', 24))
        select_button.pack(pady=(0, 20))


    def on_subject_select(self):
        subject = self.subject_combobox.get()
        if subject:
            self.subject_selected(subject)

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

    def calculate_score(self, confidence, correct_answers):
        # Convert correct answers count to a preliminary score of 0-100
        preliminary_score = (correct_answers / 10) * 100

        # Define the allowed score ranges for each confidence level
        allowed_ranges = {
            5: [(4, 8), (64, 100)],
            4: [(3, 3), (9, 9), (52, 63)],
            3: [(2, 2), (10, 10), (42, 51)],
            2: [(1, 1), (11, 13), (30, 41)],
            1: [(0, 0.5), (14, 29)],
        }

        def map_score_to_range(score, old_min, old_max, new_min, new_max):
        # Linearly map a score from the old range to the new range
            return new_min + (new_max - new_min) * (score - old_min) / (old_max - old_min)

        # Special exception for low scores
        if confidence == 1 and preliminary_score <= 20:
            return 0.5

        else if confidence == 2 and preliminary_score <= 20:
            return 1

        else if confidence == 3 and preliminary_score <= 20:
            return 2

        else if confidence == 4 and preliminary_score <= 20:
            return 3

        # Special handling for confidence 5 with score 40 or less
        else if confidence == 5 and preliminary_score <= 40:
            return map_score_to_range(preliminary_score, 0, 40, 4, 8)

        # Find the closest score within the allowed range for the given confidence
        def closest_allowed_score(score, ranges):
            closest_score = None
            min_distance = None
            for start, end in ranges:
                if start <= score <= end:
                    return score  # The score is within the range
                else:
                    # Check the distance to the start and end of the range
                    for point in [start, end]:
                        distance = abs(score - point)
                        if min_distance is None or distance < min_distance:
                            closest_score = point
                            min_distance = distance
            return closest_score

        # Get the allowed ranges for the given confidence
        ranges = allowed_ranges.get(confidence, [])

        # Calculate the final score
        final_score = closest_allowed_score(preliminary_score, ranges)
        return final_score


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
        with open('curve/dkecurve.json') as json_file:
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

