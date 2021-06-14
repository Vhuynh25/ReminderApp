def encrypt(text, shift):
    result = ""
    for x in text:
        # Encrypt uppercase characters
        if x.isupper():
            result += chr((ord(x) + shift - 65) % 26 + 65)

        # Encrypt lowercase characters
        elif x.islower():
            result += chr((ord(x) + shift - 97) % 26 + 97)

        else:
            result += x

    return result
