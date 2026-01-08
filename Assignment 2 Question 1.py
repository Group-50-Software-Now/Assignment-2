# Encryption.py

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
        if 'A' <= ch <= 'M':
            pos = (pos - shift1) % 26
        else:
            pos = (pos + (shift2 ** 2)) % 26
        return chr(pos + ord('A'))

    # other characters unchanged
    return ch

def encrypt_file(shift1, shift2):
    with open(RAW_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    encrypted = ""
    for ch in text:
        encrypted += encrypt_char(ch, shift1, shift2)

    with open(ENCRYPTED_FILE, "w", encoding="utf-8") as f:
        f.write(encrypted)



# Decryption using inverse mapping (rules unchanged)

RAW_FILE = r"D:\CDU Materials\summer semester 2025\Software Now\Assessment 2\Assign 2\raw_text.txt"
ENCRYPTED_FILE = r"D:\CDU Materials\summer semester 2025\Software Now\Assessment 2\Assign 2\encrypted_text.txt"
DECRYPTED_FILE = r"D:\CDU Materials\summer semester 2025\Software Now\Assessment 2\Assign 2\decrypted_text.txt"

from encrypt import encrypt_char

def decrypt_file(shift1, shift2):
    # Build encryption maps
    lower_map = {}
    upper_map = {}

    for c in "abcdefghijklmnopqrstuvwxyz":
        lower_map[c] = encrypt_char(c, shift1, shift2)

    for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        upper_map[c] = encrypt_char(c, shift1, shift2)

    # Reverse the maps
    inv_lower = {v: k for k, v in lower_map.items()}
    inv_upper = {v: k for k, v in upper_map.items()}

    with open(ENCRYPTED_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    decrypted = ""
    for ch in text:
        if 'a' <= ch <= 'z':
            decrypted += inv_lower[ch]
        elif 'A' <= ch <= 'Z':
            decrypted += inv_upper[ch]
        else:
            decrypted += ch

    with open(DECRYPTED_FILE, "w", encoding="utf-8") as f:
        f.write(decrypted)


def verify_decryption():
    with open(RAW_FILE, "r", encoding="utf-8") as f:
        original = f.read()

    with open(DECRYPTED_FILE, "r", encoding="utf-8") as f:
        decrypted = f.read()

    if original == decrypted:
        print("Decryption successful")
    else:
        print("Decryption failed")
