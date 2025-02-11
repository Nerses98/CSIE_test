import socket
import json
import os



# File to store data
DATA_FILE = "data_store.json"

# Initialize data file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as file:
        json.dump({}, file)
#testing
def load_data():
    """Load data from the JSON file."""
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    """Save data to the JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def handle_client(client_socket):
    while True:
        # Receive data from the client
        request = client_socket.recv(1024).decode('utf-8')
        if not request:
            break
        
        # Parse the request
        command, *args = request.split(' ', 1)
        response = ""
        data = load_data()  # Load current data

        if command == "STORE":  # Store key-value pair
            try:
                key, value = args[0].split('=', 1)
                data[key] = value
                save_data(data)
                response = f"Data stored: {key} = {value}\n"
            except ValueError:
                response = "Invalid STORE format. Use: STORE key=value\n"
        elif command == "GET":  # Retrieve value by key
            key = args[0]
            value = data.get(key, "Key not found")
            response = f"{key} = {value}\n"
        elif command == "EXIT":  # Exit the session
            response = "Hajox!\n"
            client_socket.send(response.encode('utf-8'))
            break
        elif command == "\r\n":
            response = "Invalid command. Use STORE, GET, or EXIT.\n"
        else:
            response = "Invalid command. Use STORE, GET, or EXIT.\n"
        
        client_socket.send(response.encode('utf-8'))

    client_socket.close()

def start_server(host="127.0.0.1", port=65432):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server started on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_server()
