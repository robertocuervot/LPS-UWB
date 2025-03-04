import numpy as np
import serial
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define anchor positions in 3D space (x, y, z)
anchors = {
    "an0": (0, 0, 0),
    "an1": (2, 0, 0),
    "an2": (0, 2, 0),
    "an3": (0, 0, 2)
}

def trilateration_3d(d0, d1, d2, d3):
    """Calculates the 3D position of the tag using trilateration"""
    x0, y0, z0 = anchors["an0"]
    x1, y1, z1 = anchors["an1"]
    x2, y2, z2 = anchors["an2"]
    x3, y3, z3 = anchors["an3"]
    
    A = 2 * (x1 - x0)
    B = 2 * (y1 - y0)
    C = 2 * (z1 - z0)
    D = d0**2 - d1**2 - x0**2 + x1**2 - y0**2 + y1**2 - z0**2 + z1**2
    
    E = 2 * (x2 - x0)
    F = 2 * (y2 - y0)
    G = 2 * (z2 - z0)
    H = d0**2 - d2**2 - x0**2 + x2**2 - y0**2 + y2**2 - z0**2 + z2**2
    
    I = 2 * (x3 - x0)
    J = 2 * (y3 - y0)
    K = 2 * (z3 - z0)
    L = d0**2 - d3**2 - x0**2 + x3**2 - y0**2 + y3**2 - z0**2 + z3**2
    
    matrix = np.array([[A, B, C], [E, F, G], [I, J, K]])
    values = np.array([D, H, L])
    
    try:
        position = np.linalg.solve(matrix, values)
        return position[0], position[1], position[2]
    except np.linalg.LinAlgError:
        return None

def plot_3d_position(position):
    """Plots the anchors and the estimated tag position in 3D space"""
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d') 
    # Creates a subplot within the figure
    # 111 means 1 row, 1 column, and this is the first (and only) subplot
    # Projection='3d' tells Matplotlib to create a 3D plot instead of the default 2D, this is why Axes3D  was imported
    
    # Plot anchors
    for key, (x, y, z) in anchors.items():
        ax.scatter(x, y, z, c='red', marker='o', label=key)
        ax.text(x, y, z, key, color='black')
    
    # Plot tag position
    if position:
        ax.scatter(position[0], position[1], position[2], c='blue', marker='x', label='Tag')
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('3D Trilateration Visualization')
    plt.legend()
    plt.show()

def main():
    """Main function to read serial data and compute the 3D position"""
    # Set serial port
    ser = serial.Serial('COM9', 115200, 
                        timeout=1, # 1 second timeout
                        # Maybe deactivating this was causing problems
                        # dsrdtr=False,  # Deactivates DTR to avoid reset
                        # rtscts=False   # Deactivates RTS to avoid problems with GPIO 0
                    )
    
    distances = {"an0": None, "an1": None, "an2": None, "an3": None}  # Dictionary to store distances
    
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                parts = line.split(':') # Now using split because is more efficient and the data received is consistent
                if len(parts) == 2 and parts[0] in distances:
                    anchor_id = parts[0]
                    distance = float(parts[1].replace('m', ''))  # Remove 'm' and convert to float
                    distances[anchor_id] = distance
                
                if all(distances.values()):  # Check if all distances are received
                    position = trilateration_3d(distances["an0"], distances["an1"], distances["an2"], distances["an3"])
                    if position:
                        print(f'Tag Position: {position}')
                        plot_3d_position(position)
                    distances = {"an0": None, "an1": None, "an2": None, "an3": None}  # Reset distances
        except KeyboardInterrupt:
            print("Exiting...")
            ser.close()
            break

if __name__ == "__main__":
    main()