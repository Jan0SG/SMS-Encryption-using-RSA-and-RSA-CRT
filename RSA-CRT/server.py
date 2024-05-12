import socket
import csv
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def generate_key_pair():
    # Generate RSA key with CRT parameters
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt_message(message, public_key):
    key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(key)

    if isinstance(message, str):
        message = message.encode()

    start_time = time.time()
    ciphertext = cipher.encrypt(message)
    end_time = time.time()
    encryption_time = end_time - start_time
    return ciphertext, encryption_time

def decrypt_message(ciphertext, private_key):
    key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(key)

    start_time = time.perf_counter()  # High-resolution timer
    decrypted_message = cipher.decrypt(ciphertext)
    end_time = time.perf_counter()  # High-resolution timer
    decryption_time = end_time - start_time

    decrypted_message = decrypted_message.decode()
    return decrypted_message, decryption_time

def write_to_csv(data, filename='message_logRSA-CRT.csv'):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["User", "Message", "Decryption Time (s)", "Encryption Time (s)", "Ciphertext"])
        writer.writerow(data)

def start_server():
    private_key, public_key = generate_key_pair()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('127.0.0.1', 12345))
        server_socket.listen()

        print("Entering the CHAT ZONE...")

        try:
            while True:
                client_socket, client_addr = server_socket.accept()
                print(f"Connection established with {client_addr}")

                with client_socket:
                    client_socket.sendall(public_key)
                    client_socket.recv(2048)
                    # Ask the client for a username
                    username = client_socket.recv(2048).decode('utf-8')
                    print(f"{client_addr} is now known as {username}")

                    print("Chat Log:")  # Print at the start

                    while True:
                        data = client_socket.recv(1024)

                        if not data:
                            print(f"{username} disconnected.")
                            break

                        if data.lower() == b'peace fellas':
                            print(f"{username} requested server shutdown.")
                            break

                        encrypted_message, encryption_time = encrypt_message(data.decode('utf-8'), public_key)
                        decrypted_message, decryption_time = decrypt_message(encrypted_message, private_key)

                        print(f"{username}: {decrypted_message}")

                        write_to_csv([username, decrypted_message, decryption_time, encryption_time, encrypted_message.hex()])

                        client_socket.sendall(b'ack')

        except KeyboardInterrupt:
            print("Server is shutting down due to KeyboardInterrupt. Goodbye!")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            server_socket.close()

if __name__ == "__main__":
    start_server()
