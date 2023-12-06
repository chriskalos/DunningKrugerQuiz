# import matplotlib.pyplot as plt
# import numpy as np

# def plot_score_on_curve(score):
#     # Normalize the score to be between 0 and 1
#     normalized_score = score / 100

#     # Create the Dunning-Kruger effect curve using a sigmoid function
#     x = np.linspace(0, 1, 100)
#     y = 1 / (1 + np.exp(-12 * (x - 0.5)))  # Adjust the sigmoid function to fit the curve shape
    
#     # Find the y value at the user's score position
#     user_y = 1 / (1 + np.exp(-12 * (normalized_score - 0.5)))
    
#     # Plot the curve
#     plt.plot(x, y, label="Dunning-Kruger Effect Curve")

#     # Mark the user's position
#     plt.plot(normalized_score, user_y, 'ro', label="Your Position")  # 'ro' for red dot
    
#     # Annotate the user's score on the plot
#     plt.annotate(f"Your score: {score}", (normalized_score, user_y), textcoords="offset points", xytext=(0,10), ha='center')

#     # Add labels and title
#     plt.title("Your Position on the Dunning-Kruger Effect Curve")
#     plt.xlabel("Knowledge - Experience")
#     plt.ylabel("Confidence")
#     plt.grid(True)
#     plt.legend()

#     # Show the plot
#     plt.show()

# # Example usage
# plot_score_on_curve(70)  # Example score of 70

import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, interp1d

def plot_score_on_curve(score):
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
    normalized_score = min_x + (max_x - min_x) * score / 100

    # Use the spline function to find the corresponding Y value
    user_y = spl(normalized_score)

    # Plotting the smooth curve
    plt.plot(x_new, spl(x_new))
    # Mark the user's position
    plt.plot(normalized_score, user_y, 'ro')  # 'ro' for red dot

    # Annotate the user's score on the plot
    plt.annotate(f"You are here!", (normalized_score, user_y), textcoords="offset points", xytext=(0,10), ha='center')

    # Adding annotations
    plt.text(20, 4, "Peak of Mount Stupid", horizontalalignment='center', verticalalignment='bottom')
    plt.text(27, 1.6, "Valley of Despair", horizontalalignment='center', verticalalignment='top')
    plt.text(55, 2, "Slope of Enlightenment", horizontalalignment='center', verticalalignment='bottom')
    plt.text(88, 4, "Plateau of Sustainability", horizontalalignment='center', verticalalignment='bottom')

    # Add labels and title
    plt.title("Your Position on the Dunning-Kruger Effect Curve")
    plt.xlabel("Knowledge - Experience")
    plt.ylabel("Confidence")
    plt.grid(True)

    # Show the plot
    plt.show()

plot_score_on_curve(90)  # Example score of 70