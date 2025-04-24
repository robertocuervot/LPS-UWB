import serial
import numpy as np
import csv
import time

# Define the output file
output_file = "2D_positions.csv"

# Define anchor positions in 3D space (x, y, z)
anchors = {
    "an0": (0, 0),
    "an1": (5.1, 0),
    "an2": (0, 16.7),
    "an3": (5.1, 16.7)
}

# Calculate the 2D position (x, y) using distances to known anchors via least squares.
def trilateration_2d(distances_dict):
    try:
        if len(distances_dict) < 3:
            raise ValueError("At least 3 distances are required for 2D multilateration.")

        anchor_keys = list(distances_dict.keys()) # Dictionary keys to list

        x0, y0 = anchors[anchor_keys[0]] # First anchor selected as reference
        d0 = distances_dict[anchor_keys[0]]

        # Ax = b
        A = [] # Coefficient matrix
        b = [] # Results

        # Loop for the other anchors' equations
        for i in range(1, len(anchor_keys)):
            xi, yi = anchors[anchor_keys[i]]
            di = distances_dict[anchor_keys[i]]

            Ai = [2 * (xi - x0), 2 * (yi - y0)]
            bi = d0**2 - di**2 - x0**2 + xi**2 - y0**2 + yi**2

            A.append(Ai)
            b.append(bi)

        A = np.array(A)
        b = np.array(b)

        # Solve the linear system using least-squares because no exact solution exists as the system is overdetermined
        # position = Least Squares solution
        # residuals = sum of squared residuals
        # rank = rank of matrix A
        # s = singular values of matrix A
        position, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
        return position[0], position[1]

    except Exception as e:
        print(f"[ERROR] multilateration_2d: {e}")
        return None
    

def main():
    # Write header to CSV file
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "X", "Y", "Z"])  # Header row

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
                    distance = float(parts[1].replace('m', ''))  # Remove the 'm' and convert to float
                    distances[anchor_id] = distance
                    # print("Dsitances:\n", distances)
                
                if all(distances.values()):  # Check if all distances are received
                    # print("Data received correctly")
                    position = trilateration_2d(distances) # Call the multilateration function
                    # print("Position:\n", position)
                    if position:
                        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp
                        print(f"[{timestamp}] Position: X={position[0]:.2f}, Y={position[1]:.2f}")

                        # Save to CSV
                        with open(output_file, mode="a", newline="") as file:
                            writer = csv.writer(file)
                            writer.writerow([timestamp, position[0], position[1], 0]) # z=0
                    
                    distances = {"an0": None, "an1": None, "an2": None, "an3": None}  # Reset distances
        except KeyboardInterrupt:
            print("Exiting...")
            ser.close()
            break

if __name__ == "__main__":
    main()