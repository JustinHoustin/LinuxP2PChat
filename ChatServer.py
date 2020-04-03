import socket
import sys
import threading
import os


class Server(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen()
        print("Waiting for connection...")
        s, address = self.sock.accept()

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
                    print(client_name + " has ended the chat")
                    os._exit(0)
                message = encode_emojis(message)
                print(client_name + ": " + message)

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
                print(server_name + ": " + message)

        server_name = input("What is your name? ")
        print("Please wait...")
        s.sendall(server_name.encode())
        client_name = s.recv(1024).decode()
        print("Connected!")
        print("Type --list at any point to receive a list of emoji codes.")
        print("Type --quit to leave the chat")
        threading.Thread(target=sent).start()
        threading.Thread(target=send).start()


if __name__ == "__main__":
    while True:
        port_num = input("Enter Port Number -> ")
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass

    print("The server is now running on port %d." % port_num)
    Server('', port_num).listen()
