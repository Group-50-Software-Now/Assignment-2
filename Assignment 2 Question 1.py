"""
encrypt.py
----------
This file encrypts the content inside raw_text.txt and saves the encrypted result
into encrypted_text.txt.

The encryption follows the given rules:
- Lowercase letters are treated differently depending on if they are in a-m or n-z
- Uppercase letters are treated differently depending on if they are in A-M or N-Z
- All other characters (space, punctuation, etc.) stay unchanged
"""

import os

# Finding the folder where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Making full file paths so it works on any machine
RAW_FILE = os.path.join(BASE_DIR, "raw_text.txt")
ENCRYPTED_FILE = os.path.join(BASE_DIR, "encrypted_text.txt")


def encrypt_char(ch: str, shift1: int, shift2: int) -> str:
    """
    Encrypts a single character based on the provided rules.

    The alphabet is split into halves of 13 letters:
    - a-m and n-z
    - A-M and N-Z

    This is why we use % 13 (wrap around inside the half).
    """

    # ----- lowercase letters -----
    if "a" <= ch <= "m":
        # a-m is 13 letters, so offset will be 0..12
        offset = ord(ch) - ord("a")
        s = (shift1 * shift2) % 13
        new_offset = (offset + s) % 13
        return chr(ord("a") + new_offset)

    if "n" <= ch <= "z":
        # n-z is also 13 letters
        offset = ord(ch) - ord("n")
        s = (shift1 + shift2) % 13
        new_offset = (offset - s) % 13
        return chr(ord("n") + new_offset)

    # ----- uppercase letters -----
    if "A" <= ch <= "M":
        offset = ord(ch) - ord("A")
        s = shift1 % 13
        new_offset = (offset - s) % 13
        return chr(ord("A") + new_offset)

    if "N" <= ch <= "Z":
        offset = ord(ch) - ord("N")
        s = (shift2 ** 2) % 13
        new_offset = (offset + s) % 13
        return chr(ord("N") + new_offset)

    # ----- other characters unchanged -----
    return ch


def encrypt_file(shift1: int, shift2: int) -> None:
    """
    Reads raw_text.txt, encrypts it using encrypt_char(),
    and writes the encrypted result to encrypted_text.txt.
    """

    # Reading original text file
    with open(RAW_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    # Encrypting character by character
    encrypted = "".join(encrypt_char(ch, shift1, shift2) for ch in text)

    # Writing encrypted result to output file
    with open(ENCRYPTED_FILE, "w", encoding="utf-8") as f:
        f.write(encrypted)


#decryption.py

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

"""
main.py

This is the entry point of the program.
It collects user input, runs encryption,
then performs decryption and verification.
"""

from encrypt import encrypt_file
from decrypt import decrypt_file, verify_decryption

print("=== Encryption and Decryption Program ===")

shift1 = int(input("Enter shift1 value: "))
shift2 = int(input("Enter shift2 value: "))

encrypt_file(shift1, shift2)
print("Encryption completed.")

decrypt_file(shift1, shift2)
print("Decryption completed.")

verify_decryption()
