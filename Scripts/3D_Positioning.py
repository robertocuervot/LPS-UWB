import serial
import numpy as np
import csv
import time

# Define the output file
output_file = "positions.csv"

# Write header to CSV file
with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "X", "Y", "Z"])  # Header row

# Define anchor positions in 3D space (x, y, z)
anchors = {
    "an0": (0, 0, 1.9),
    "an1": (0, 19.4, 0),
    "an2": (6, 0, 0),
    "an3": (6, 19.4, 1.9)
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

def main():
    """Main function to read serial data and compute the 3D position"""
    # Set serial port
    ser = serial.Serial('COM9', 115200, # COM9: tag 0; COM11: tag 1
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
                    # print("Dsitances:\n", distances)
                
                if all(distances.values()):  # Check if all distances are received
                    # print("Data received correctly")
                    position = trilateration_3d(distances["an0"], distances["an1"], distances["an2"], distances["an3"])
                    # print("Position:\n", position)
                    if position:
                        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp
                        print(f"[{timestamp}] Position: X={position[0]:.2f}, Y={position[1]:.2f}, Z={position[2]:.2f}")

                        # Save to CSV
                        with open(output_file, mode="a", newline="") as file:
                            writer = csv.writer(file)
                            writer.writerow([timestamp, position[0], position[1], position[2]])
                    
                    distances = {"an0": None, "an1": None, "an2": None, "an3": None}  # Reset distances
        except KeyboardInterrupt:
            print("Exiting...")
            ser.close()
            break

if __name__ == "__main__":
    main()