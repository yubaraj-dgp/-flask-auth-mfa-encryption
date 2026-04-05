def encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            result += chr((ord(char) + shift - 65) % 26 + 65)
        else:
            result += char
    return result

def decrypt(text, shift):
    return encrypt(text, -shift)