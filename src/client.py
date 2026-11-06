import socket
import threading

connection_closed = threading.Event()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM
client_socket.connect(("127.0.0.1", 5000))
print("Connected to server!")


#sending message to server
def send_message(message):
    client_socket.send(message.encode())

message = input("You: ")
send_message(message)
print("Message sent!")


##response from server
def receive_loop():

    while True:
        try:
            data = client_socket.recv(1024)

            if not data:
                if not connection_closed.is_set():
                    print("Server disconnected!")

                connection_closed.set()
                break

            print("Server:", data.decode())

        except OSError as e:

            if not connection_closed.is_set():
                print("Connection error:", e)

            connection_closed.set()
            break




receive_thread = threading.Thread(target=receive_loop, daemon=True)

receive_thread.start()


while True:

    if connection_closed.is_set():
        print("Cannot send. Server is disconnected.")
        break

    message = input("You: ")

    if connection_closed.is_set():
        print("Server disconnected. Message not sent.")
        break

    if message.lower() == "exit":
        break

    try:
        client_socket.sendall(message.encode())

    except OSError:
        print("Failed to send. Connection is closed.")
        break


    
connection_closed.set()

try:
    client_socket.shutdown(socket.SHUT_RDWR)
except OSError:
    pass

client_socket.close()

receive_thread.join()

print("Connection closed.")
