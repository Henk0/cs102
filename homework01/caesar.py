def encrypt_caesar(plaintext, shift):
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for char in plaintext:
    	if "A" <= char <= "Z" or "a" <= char <= "z":
    		enc = ord(char) + int(shift)
    		if (enc > ord("Z") and enc < ord("a")) or enc > ord("z"):
    			enc -= 26
    		char = chr(enc)
    	ciphertext += char		
    return ciphertext


def decrypt_caesar(ciphertext, shift):
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for char in ciphertext:
    	if "A" <= char <= "Z" or "a" <= char <= "z":
    		enc = ord(char) - int(shift)
    		if enc < ord("A") or (enc > ord("Z") and enc < ord("a")):
    			enc += 26
    		char = chr(enc)
    	plaintext += char
    return plaintext
    