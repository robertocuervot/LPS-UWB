import serial
import re

# Set serial port
ser = serial.Serial('COM9', 115200, # COM9: tag 0; COM11: tag 1
                    timeout=1, # 1 second timeout
                    # dsrdtr=False,  # Deactivates DTR to avoid reset
                    # rtscts=False   # Deactivates RTS to avoid problems with GPIO 0
                    )

# Extract distance values from the structure they com with when printing in serial
pattern = re.compile(r"an(\d):([\d.]+)m")

# To save last readings
last_readings = {"an0": None, "an1": None, "an2": None, "an3": None}

while True:
    if ser.in_waiting:
        line = ser.readline().decode().strip()
        # print("Line: ", line)
        matches = pattern.findall(line)
        # print("Matches: ", matches)

        if matches:
            for anchor, distance in matches:
                key = f"an{anchor}"
                value = float(distance)
                print(f"{key}: {value} m")

        #         # Only update if the value changed
        #         if last_readings[key] != value:
        #             last_readings[key] = value
        #             print(f"{key}: {value} m")  # Print updated values