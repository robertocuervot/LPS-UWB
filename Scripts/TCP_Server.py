import socket

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 8888       # Port used in M5 Atom

BUFFER_SIZE = 1024  # Size of each chunk of incoming data

# Create TCP server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Optional: allow reusing the port if it was recently closed
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind to IP and port
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Listening on {HOST}:{PORT}...")


try:
    # Wait for a client (M5 Atom) to connect
    conn, addr = server_socket.accept()
    print(f"Connection established with {addr}")

    distances = {"an0": None, "an1": None, "an2": None, "an3": None}  # Dictionary to store distances

    while True:
        data = conn.recv(BUFFER_SIZE).decode('utf-8').strip()
        if data:
            print(f"Received: {data}")
            parts = data.split(':') # Now using split because is more efficient and the data received is consistent
            if len(parts) == 2 and parts[0] in distances:
                anchor_id = parts[0]
                distance = float(parts[1].replace('m', ''))  # Remove the 'm' and convert to float
                distances[anchor_id] = distance
                print("Dsitances:\n", distances)
except KeyboardInterrupt:
    print("\nServer manually stopped.")
finally:
    conn.close()
    server_socket.close()
    print("Connection closed.")