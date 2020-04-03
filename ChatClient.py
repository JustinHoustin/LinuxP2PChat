import socket
import sys
import threading
import os


def client():

    s = socket.socket()

    # this method is intended to recieve a list of files in the directory the server is currently in
    def list_emojis():
        print("\U00002605: :star:")
        print("\U0001F603: :smile:")
        print("\U0001F602: :joy:")
        print("\U0001F609: :wink:")
        print("\U0001F60D: :love:")
        print("\U0001F62C: :yikes:")
        print("\U0001F62E: :shock:")

    def encode_emojis(message):
        message = message.replace(":star:", "\U00002605")
        message = message.replace(":smile:", "\U0001F603")
        message = message.replace(":joy:", "\U0001F602")
        message = message.replace(":wink:", "\U0001F609")
        message = message.replace(":love:", "\U0001F60D")
        message = message.replace(":yikes:", "\U0001F62C")
        message = message.replace(":shock:", "\U0001F62E")
        return message

    def sent():
        while True:
            message = s.recv(4096).decode()
            if not message:
                sys.exit(0)
            if message == '--quit':
                print(server_name + " has ended the chat")
                os._exit(0)
            message = encode_emojis(message)
            print(server_name + ": " + message)

    def send():
        cursor_up_one = '\x1b[1A'
        erase_line = '\x1b[2K'
        while True:
            message = input()
            if not message:
                sys.exit(0)
            if message == '--quit':
                s.sendall(message.encode())
                os._exit(0)
            if message == '--list':
                list_emojis()
                continue
            sys.stdout.write(cursor_up_one)
            sys.stdout.write(erase_line)
            s.sendall(message.encode())
            message = encode_emojis(message)
            print(client_name + ": " + message)

    ip = input("Enter in the IP address that you wish to connect to: ")
    port = input("Enter in the Port Number: ")
    connector(s, ip, port)
    client_name = input("What is your name? ")
    print("Please wait...")
    s.sendall(client_name.encode())
    server_name = s.recv(1024).decode()
    print("Connected!")
    print("Type --list at any point to receive a list of emoji codes.")
    print("Type --quit to leave the chat")

    threading.Thread(target=sent).start()
    threading.Thread(target=send).start()
    return s


def connector(the_socket, IP, socketPort):
    HOST = IP
    PORT = int(socketPort)
    the_socket.connect((HOST, PORT))


client()
