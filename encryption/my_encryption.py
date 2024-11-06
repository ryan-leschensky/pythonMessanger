class MyEncryption:
    @staticmethod
    def encrypt(message, key):
        message = message.lower()
        key = int(key)

        start = ord('a')
        end = ord('z')

        cookie = "jadenlosthiscookies"
        key = key % len(cookie)

        start_char = cookie[key]

        shift = ord(start_char) - start

        cipher_text = ""

        print(shift)

        for i in range(len(message)):
            new_char = chr((ord(message[i]) + shift - end ) % (end - start) + start)
            cipher_text += new_char

        return cipher_text

    @staticmethod
    def decrypt(message, key):
        message = message.lower()
        key = int(key)

        start = ord('a')
        end = ord('z')

        cookie = "jadenlosthiscookies"
        key = key % len(cookie)

        start_char = cookie[key]

        shift = ord(start_char) - start

        cipher_text = ""

        print(shift)

        for i in range(len(message)):
            new_char = chr((ord(message[i]) - shift - end) % (end - start) + start)
            cipher_text += new_char

        return cipher_text
