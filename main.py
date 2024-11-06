from encryption.my_encryption import MyEncryption
from networking.my_server import MyServer
from networking.my_client import MyClient
import tkinter as tk
import threading


class ChatApp:
    def __init__(self, window, port, key, is_server):
        self.send_button = None
        self.message_entry = None
        self.chat_history = None
        self.window = window
        self.port = int(port)
        self.is_server = is_server
        self.key = int(key)
        self.conn = None

        self.setup_gui()

        if is_server:
            self.server = MyServer(port=self.port, key=self.key)
            threading.Thread(target=self.server.start, args=(self,)).start()
        else:
            self.client = MyClient(port=self.port, key=self.key)
            threading.Thread(target=self.client.start, args=(self,)).start()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_gui(self):
        self.chat_history = tk.Text(self.window, state='disabled', width=50, height=20)
        self.chat_history.pack(pady=10)

        self.message_entry = tk.Entry(self.window, width=40)
        self.message_entry.pack(side=tk.LEFT, padx=10)

        self.send_button = tk.Button(self.window, text="Send", width=10, command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=10)

    def append_message(self, message):
        self.chat_history.config(state='normal')
        self.chat_history.insert(tk.END, message + '\n')
        self.chat_history.config(state='disabled')
        self.chat_history.yview(tk.END)

    def send_message(self):
        message = self.message_entry.get()
        self.append_message(f"You: {message}")
        self.message_entry.delete(0, tk.END)

        try:
            encrypted_message = MyEncryption.encrypt(message, self.key)
            if self.is_server and self.conn:
                self.conn.sendall(encrypted_message.encode())
            elif self.client.sock:
                self.client.sock.sendall(encrypted_message.encode())
            else:
                self.append_message("Connection not established yet.")
        except AttributeError:
            self.append_message("Connection not established yet.")
        except Exception as e:
            self.append_message(f"Error sending message: {e}")

    def receive_message_server(self, decrypted_message):
        self.append_message(f"Client: {decrypted_message}")

    def receive_message_client(self, decrypted_message):
        self.append_message(f"Server: {decrypted_message}")

    def initialize_server_connection(self, conn):
        self.conn = conn
        self.append_message("Server: Connection established")

    def initialize_client_socket(self, sock):
        self.client.sock = sock
        self.append_message("Client: Connected to server.")

    def on_closing(self):
        if self.is_server:
            self.server.running = False
            if self.server.conn:
                self.server.conn.close()
        else:
            self.client.running = False
            if self.client.sock:
                self.client.sock.close()
        self.window.destroy()


def start_chat_app(port, key, role):
    try:
        port = int(port)
        key = int(key)
    except ValueError:
        print("Invalid port number or key. Please enter valid integers.")
        return

    root = tk.Tk()
    root.title("Chat Application")
    ChatApp(root, port, key, role == "server")
    root.mainloop()


def main():
    window = tk.Tk()
    window.title("Select Mode")

    tk.Label(window, text="Select mode:").pack(pady=10)

    tk.Label(window, text="Port:").pack(pady=5)
    port_entry = tk.Entry(window)
    port_entry.pack(pady=5)

    tk.Label(window, text="Encryption Key:").pack(pady=5)
    key_entry = tk.Entry(window)
    key_entry.pack(pady=5)

    server_button = tk.Button(window, text="Run Server",
                              command=lambda: start_chat_app(port_entry.get(), key_entry.get(), "server"))
    server_button.pack(pady=5)

    client_button = tk.Button(window, text="Run Client",
                              command=lambda: start_chat_app(port_entry.get(), key_entry.get(), "client"))
    client_button.pack(pady=5)

    window.mainloop()


if __name__ == '__main__':
    main()