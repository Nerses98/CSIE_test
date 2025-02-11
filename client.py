import socket

def start_client(host="127.0.0.1", port=65432):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    print("Connected to the server. Use commands: STORE key=value, GET key, EXIT")
    while True:
        command = input("> ")
        client.send(command.encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
        print(response)
        if command.strip().upper() == "EXIT":
            break

    client.close()

if __name__ == "__main__":
    start_client()
    
#skdugbkfdsj
