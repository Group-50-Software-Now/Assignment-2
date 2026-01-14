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

# ----- uppercase N-Z -----
    if "N" <= ch <= "Z":
        offset = ord(ch) - ord("N")
        s = (shift2 ** 2) % 13
        new_offset = (offset - s) % 13
        return chr(ord("N") + new_offset)

    # If it is not a letter, we just return it as it is
    return ch


def decrypt_file(shift1: int, shift2: int) -> None:
    """
    Reads encrypted_text.txt, decrypts each character using decrypt_char(),
    and writes the result into decrypted_text.txt.
    """

    # Reading encrypted file contents
    with open(ENCRYPTED_FILE, "r", encoding="utf-8") as f:
        encrypted_text = f.read()

    # Decrypting every character one by one
    decrypted = "".join(decrypt_char(ch, shift1, shift2) for ch in encrypted_text)

    # Saving the decrypted text into a new file
    with open(DECRYPTED_FILE, "w", encoding="utf-8") as f:
        f.write(decrypted)


def verify_decryption() -> bool:
    """
    Compares raw_text.txt and decrypted_text.txt.

    Returns:
        True  -> if they match exactly
        False -> if they are different
    """

    # Reading the original raw file
    with open(RAW_FILE, "r", encoding="utf-8") as f:
        original = f.read()

    # Reading the decrypted file
    with open(DECRYPTED_FILE, "r", encoding="utf-8") as f:
        decrypted = f.read()

    # Checking if both are exactly the same
    if original == decrypted:
        print("Decryption successful: files match exactly.")
        return True

    print("Decryption failed: files do not match.")
    return False

"""
main.py
-------
This is the main program file.

It:
1) asks the user for shift1 and shift2
2) encrypts raw_text.txt into encrypted_text.txt
3) decrypts encrypted_text.txt into decrypted_text.txt
4) verifies whether decrypted_text matches raw_text exactly
"""

from encrypt import encrypt_file
from decrypt import decrypt_file, verify_decryption


def get_int(prompt: str) -> int:
    """
    Keeps asking the user until they enter a valid integer.

    This prevents the program from crashing if the user types letters by mistake.
    """
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")


print("=== Encryption and Decryption Program ===")

# Taking user inputs safely
shift1 = get_int("Enter shift1 value: ")
shift2 = get_int("Enter shift2 value: ")

# Encrypting the raw file
encrypt_file(shift1, shift2)
print("Encryption completed.")

# Decrypting back into decrypted_text.txt
decrypt_file(shift1, shift2)
print("Decryption completed.")

# Checking if decryption worked correctly
verify_decryption()
