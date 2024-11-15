import socket
from threading import Thread
from encryption.my_encryption import MyEncryption


class MyClient:
    def __init__(self, host='10.110.33.22', port=65432, key=3):
        self.host = host
        self.port = port
        self.key = key
        self.sock = None
        self.running = False

    def receive_messages(self, chat_app):
        try:
            while self.running:
                data = self.sock.recv(1024)
                if not data:
                    break
                decrypted_message = MyEncryption.decrypt(data.decode(), self.key)
                print(f"Received from server: {decrypted_message}")
                chat_app.receive_message_client(decrypted_message)
        except Exception as e:
            print(f"Error receiving messages: {e}")
        finally:
            print("Disconnected from server")
            self.sock.close()
            self.running = False

    def start(self, chat_app, *args, **kwargs):
        self.running = True
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.sock = s
            try:
                s.connect((self.host, self.port))
                print(f"Connected to {self.host}:{self.port}")
                chat_app.initialize_client_socket(self.sock)

                receiver_thread = Thread(target=self.receive_messages, args=(chat_app,))
                receiver_thread.start()

                while self.running:
                    pass

                receiver_thread.join()  # Ensure the receiver thread finishes
                print("Client shutdown")
                chat_app.append_message("Client shutdown")
            except ConnectionError as ce:
                print(f"Connection error: {ce}")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                s.close()