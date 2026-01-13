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

"""
decrypt.py
----------
This file is used to decrypt the encrypted_text.txt file back into decrypted_text.txt.

It works by reversing the same rules that were used in encrypt.py.
After decryption, another function can compare decrypted_text.txt with raw_text.txt
to check if the decryption worked correctly.
"""

import os

# Getting the folder location where this python file is saved
# (this helps so the program can find the text files easily)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Building full file paths so it works on any computer as long as files are in the same folder
RAW_FILE = os.path.join(BASE_DIR, "raw_text.txt")
ENCRYPTED_FILE = os.path.join(BASE_DIR, "encrypted_text.txt")
DECRYPTED_FILE = os.path.join(BASE_DIR, "decrypted_text.txt")


def decrypt_char(ch: str, shift1: int, shift2: int) -> str:
    """
    Decrypt one single character using the reverse (opposite) of encrypt_char rules.

    Rules used here:
    - Lowercase a-m are wrapped inside 13 letters (a..m)
    - Lowercase n-z are wrapped inside 13 letters (n..z)
    - Uppercase A-M are wrapped inside 13 letters (A..M)
    - Uppercase N-Z are wrapped inside 13 letters (N..Z)

    Any non-letter characters (spaces, punctuation, numbers) are returned unchanged.
    """

    # ----- lowercase a-m -----
    if "a" <= ch <= "m":
        offset = ord(ch) - ord("a")
        s = (shift1 * shift2) % 13
        new_offset = (offset - s) % 13
        return chr(ord("a") + new_offset)

    # ----- lowercase n-z -----
    if "n" <= ch <= "z":
        offset = ord(ch) - ord("n")
        s = (shift1 + shift2) % 13
        new_offset = (offset + s) % 13
        return chr(ord("n") + new_offset)

    # ----- uppercase A-M -----
    if "A" <= ch <= "M":
        offset = ord(ch) - ord("A")
        s = shift1 % 13
        new_offset = (offset + s) % 13
        return chr(ord("A") + new_offset)

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
