from my_encryption import MyEncryption
import tkinter as tk

if __name__ == '__main__':
    def set_encrypt():
        cipher_text = MyEncryption.encrypt(text_input.get(), key_input.get())
        text_input.delete(0, tk.END)
        text_input.insert(0, cipher_text)


    def set_decrypt():
        plain_text = MyEncryption.decrypt(text_input.get(), key_input.get())
        text_input.delete(0, tk.END)
        text_input.insert(0, plain_text)


    window = tk.Tk()
    window.title("Text Encryptor")

    tk.Label(window, text="Text Input:").grid(row=0, column=0, padx=10, pady=10)
    text_input = tk.Entry(window, width=30)
    text_input.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(window, text="Key:").grid(row=1, column=0, padx=10, pady=10)
    key_input = tk.Entry(window, width=30)
    key_input.grid(row=1, column=1, padx=10, pady=10)

    encrypt_button = tk.Button(window, text="Encrypt", command=set_encrypt)
    encrypt_button.grid(row=2, column=0, padx=10, pady=10, sticky="e")

    decrypt_button = tk.Button(window, text="Decrypt", command=set_decrypt)
    decrypt_button.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    window.mainloop()
