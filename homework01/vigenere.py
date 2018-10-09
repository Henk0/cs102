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
    	if "A" <= plaintext[i] <= "Z" or "a" <= plaintext[i] <= "z":
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
    	else:
    		ciphertext += plaintext[i] 
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
    plaintext = ""
    for i in range(len(ciphertext)):
    	if "A" <= ciphertext[i] <= "Z" or "a" <= ciphertext[i] <= "z":
    		shift = keyword[i % len(keyword)]
    		if shift <= "Z":
    			shift = ord(shift) - ord("A")
    		else:
    			shift = ord(shift) - ord("a")
    		symbol = ord(ciphertext[i]) - shift
    		if "a" <= ciphertext[i] <= "z" and symbol < ord("a"):
    			symbol += 26
    		elif symbol < ord("A"):
    			symbol += 26
    		plaintext += chr(symbol)
    	else:
    		plaintext += ciphertext[i]	
    return plaintext
