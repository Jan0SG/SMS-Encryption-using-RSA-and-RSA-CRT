import socket

def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('127.0.0.1', 12345))

        public_key = client_socket.recv(2048)

        # Ask the user to choose a username
        username = input("Choose your username: ").encode('utf-8')
        client_socket.sendall(username)

        while True:
            # Take user input for the message
            message = input("Type your message (or 'exit' to quit): ").encode('utf-8')

            # Send the message to the server
            client_socket.sendall(message)

            # Check if the user wants to exit
            if message.lower() == b'peace fellas':
                break

        # Explicitly close the socket after the loop
        client_socket.close()

if __name__ == "__main__":
    start_client()
