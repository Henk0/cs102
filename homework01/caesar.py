def encrypt_caesar(plaintext, shift):
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON", 3)
    'SBWKRQ'
    >>> encrypt_caesar("python", 3)
    'sbwkrq'
    >>> encrypt_caesar("Python3.6", 3)
    'Sbwkrq3.6'
    >>> encrypt_caesar("", 3)
    ''
    """
    ciphertext = ""
    for char in plaintext:
        if "A" <= char <= "Z" or "a" <= char <= "z":
            symbol = ord(char) + int(shift) % 26
            if "A" <= char <= "Z" and chr(symbol) > "Z":
                symbol -= 26
            elif chr(symbol) > "z":
                symbol -= 26
            char = chr(symbol)
        ciphertext += char
    return ciphertext


def decrypt_caesar(ciphertext, shift):
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ", 3)
    'PYTHON'
    >>> decrypt_caesar("sbwkrq", 3)
    'python'
    >>> decrypt_caesar("Sbwkrq3.6", 3)
    'Python3.6'
    >>> decrypt_caesar("", 5)
    ''
    """
    plaintext = ""
    for char in ciphertext:
        if "A" <= char <= "Z" or "a" <= char <= "z":
            enc = ord(char) - int(shift) % 26
            if enc < ord("A"):
                enc += 26
            if "a" <= char <= "z" and enc < ord("a"):
                enc += 26
            char = chr(enc)
        plaintext += char
    return plaintext
