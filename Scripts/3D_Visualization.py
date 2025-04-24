import time
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation

# Path to your CSV file // positions_tag1_25.csv // positions_tag_0_10.csv
csv_file = "positions_tag_0_10.csv"

# Define static limits for the axes
X_LIM = (-2, 8)  # Example: X-axis from 0 to 10 meters
Y_LIM = (-2, 22)  # Example: Y-axis from 0 to 10 meters
Z_LIM = (-2, 2.5)   # Example: Z-axis from 0 to 3 meters (height)

# Define anchor positions in 3D space (x, y, z)
anchors = {
    "an0": (0, 0, 1.9),
    "an1": (0, 19.4, 0),
    "an2": (6, 0, 0),
    "an3": (6, 19.4, 1.9)
}

# Initialize figure and 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d') # Subplot for more flexibility if in the future I want to add another plot

# Function to update the plot
def update(frame):
    ax.clear()  # Clear previous points

    # Plot anchors
    for key, (x, y, z) in anchors.items():
        ax.scatter(x, y, z, c='black', marker='o', label=key)
        ax.text(x, y, z, key, color='black')

    try:
        # Read the CSV file
        df = pd.read_csv(csv_file)

        # Check if there is data to plot
        if df.empty:
            return
        
        # Extract X, Y, Z coordinates
        x = df['X']
        y = df['Y']
        z = df['Z']

        # Plot the trajectory
        ax.plot(x, y, z, marker='o', linestyle='-', color='b', label="Tag Path")

        # Plot the last position in a different color
        ax.scatter(x.iloc[-1], y.iloc[-1], z.iloc[-1], color='red', marker='x', s=100, label="Current Position")

        # Labels and title
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        ax.set_title("Real-Time 3D Position Tracking")
        ax.legend()

        # Set static axis limits
        # ax.set_xlim(X_LIM)
        # ax.set_ylim(Y_LIM)
        # ax.set_zlim(Z_LIM)

    except Exception as e:
        print("Error reading CSV file:", e)


# Animate the plot (updates every second)
ani = FuncAnimation(fig, update, interval=500)

plt.show()
