# Encryption.py

## Encryption rules exactly as given in the question

RAW_FILE = r"D:\CDU Materials\summer semester 2025\Software Now\Assessment 2\Assign 2\raw_text.txt"
ENCRYPTED_FILE = r"D:\CDU Materials\summer semester 2025\Software Now\Assessment 2\Assign 2\encrypted_text.txt"

def encrypt_char(ch, shift1, shift2):
    # lowercase letters
    if 'a' <= ch <= 'z':
        pos = ord(ch) - ord('a')
        if 'a' <= ch <= 'm':
            pos = (pos + shift1 * shift2) % 26
        else:
            pos = (pos - (shift1 + shift2)) % 26
        return chr(pos + ord('a'))

    # uppercase letters
    if 'A' <= ch <= 'Z':
        pos = ord(ch) - ord('A')
