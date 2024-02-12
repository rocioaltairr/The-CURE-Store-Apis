"""
Module: encrypt.py
Description: This module implements the AES algorithm for encrypting passwords, primarily for use in a store application's user authentication system.

The primary purpose of this module is to provide secure storage of user passwords. When a user creates an account, their password is encrypted using the AES algorithm and stored in the application's database. This encryption ensures that even if an attacker gains access to the database, they cannot retrieve the original passwords.

The `encrypted_password` function takes a plaintext password as input, encrypts it using AES in CBC mode with a predefined initialization vector (IV), and then base64 encodes the encrypted message before returning it. This encrypted password is then stored securely in the database.

Conversely, the `decrypt_password` function is used during the login process. It takes the encrypted password stored in the database, decrypts it using the same AES algorithm and IV, and then compares it with the plaintext password provided by the user during login. If the decrypted password matches the user's input, access is granted.

It's important to note that this encryption scheme helps mitigate the risk of unauthorized access to user passwords, enhancing the overall security of the application.
"""
import hashlib
import base64
from Crypto.Cipher import AES

def pad_message(message):
    """
    To ensure the message is 32 bytes
    """
    while len(message) % 16 != 0:
        message = message + " "
    return message

def encrypted_password(message):
    """
    To encrypt the password
    """
    password = "mypassword".encode()
    key = hashlib.sha256(password).digest()
    iv = 'This is an IV456'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad_message(message)
    encrypted_message = cipher.encrypt(padded_message)
    encrypted_message_base64 = base64.b64encode(encrypted_message).decode()
    return  encrypted_message_base64

def decrypt_password(encrypted):
    """
    To decrypt the password
    """
    password = b'mypassword'  
    key = hashlib.sha256(password).digest()
    iv = 'This is an IV456'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_message_bytes = base64.b64decode(encrypted)
    decrypted_text = cipher.decrypt(encrypted_message_bytes).strip().decode()
    return decrypted_text

# message = "Yo no lo se"
# print(encrypted_password(message))
# encrypeted_message = encrypted_password("message")
# print(decrypt_password("encrypeted_message"))
