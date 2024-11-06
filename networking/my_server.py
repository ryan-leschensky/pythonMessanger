import socket
from threading import Thread
from encryption.my_encryption import MyEncryption


class MyServer:
    def __init__(self, host='127.0.0.1', port=65432, key=3):
        self.host = host
        self.port = port
        self.key = key
        self.conn = None
        self.running = False

    def receive_messages(self, chat_app):
        try:
            while self.running:
                data = self.conn.recv(1024)
                if not data:
                    break
                decrypted_message = MyEncryption.decrypt(data.decode(), self.key)
                print(f"Received from client: {decrypted_message}")
                chat_app.receive_message_server(decrypted_message)
        except Exception as e:
            print(f"Error receiving messages: {e}")
        finally:
            print("Client disconnected")
            self.conn.close()
            self.running = False

    def start(self, chat_app, *args, **kwargs):
        self.running = True
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"Server listening on {self.host}:{self.port}")

            self.conn, addr = s.accept()
            with self.conn:
                print(f"Connected by {addr}")
                chat_app.initialize_server_connection(self.conn)

                receiver_thread = Thread(target=self.receive_messages, args=(chat_app,))
                receiver_thread.start()

                while self.running:
                    pass

                receiver_thread.join()  # Ensure the receiver thread finishes
                print("Server shutdown")
                chat_app.append_message("Server shutdown")