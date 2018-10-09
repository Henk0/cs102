def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    for i in range(len(plaintext)):
    	shift = keyword[i % len(keyword)]
    	if shift <= "Z":
    		shift = ord(shift) - ord("A")
    	else:
    		shift = ord(shift) - ord("a")
    	symbol = ord(plaintext[i]) + shift
    	if "A" < plaintext[i] < "Z" and chr(symbol) > "Z":
    		symbol -= 26
    	if chr(symbol) > "z":
    		symbol -= 26
    	ciphertext += chr(symbol) 
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    # PUT YOUR CODE HERE
    return plaintext
print(ord("a"))