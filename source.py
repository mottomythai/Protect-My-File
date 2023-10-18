import random
import os
import string
import hashlib
import time
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

# Min 100 bit hash
def hashing(password):
    hash = hashlib.md5(password.encode())
    return hash.hexdigest()

def pass_input(choice):
    password = input('Input password: ')

    with open('pass.txt', 'r') as fr:
        storedhash = fr.read()

    newhash = hashing(password)

    if choice == '1':
        if os.path.getsize('pass.txt') != 1:
            ans = input('Password is already stored. Create new password? (Y/n) ')
            if ans == 'n' or ans == 'N':
                return

        with open('pass.txt', 'w') as fw:
            fw.write(newhash)

    if choice == '2':
        # Check if the key is matching
        if os.path.getsize('pass.txt') == 1:
            print('No password saved!')
            return -1

        if newhash != storedhash:
            print('Wrong password')
            return -1

# New encrypted file content each time
def add_timestamp(filepath):
    nowtime = time.time()

    with open(filepath, 'a') as f:
        f.write(str(nowtime))

def del_timestamp(filepath):
    with open(filepath, 'r') as fr:
        mess = fr.readlines()

    mess = mess[:-1]
    
    with open(filepath, 'w') as fw:
        fw.writelines(mess)

# File encryption/decryption
def generate_passkey():
    with open('pass.txt', 'rb') as f:
        password = f.read() 

    salt = os.urandom(16)

    kdf = PBKDF2HMAC(

        algorithm=hashes.SHA256(),

        length=32,

        salt=salt,

        iterations=480000,

    )

    return base64.urlsafe_b64encode(kdf.derive(password))

def encrypt(filepath):
    add_timestamp(filepath)

    with open(filepath, 'rb') as fr:
        data = fr.read()
    
    key = generate_passkey()

    with open('key.txt', 'wb') as fk:
        fk.write(key)

    fernet = Fernet(key)
    result = fernet.encrypt(data)

    with open(filepath, 'wb') as fw:
        fw.write(result)

    print('File is encrypted!')

def decrypt(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()

    with open('key.txt', 'rb') as rk:
        key = rk.read()

    fernet = Fernet(key)
    result = fernet.decrypt(data)

    with open(filepath, 'wb') as fw:
        fw.write(result)

    del_timestamp(filepath)

    print('File is decrypted!')

# Required OTP anytime the program run
def OTP():
    with open('otp.txt', 'w') as f:
        f.write(''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(8)))

def input_otp():
    print('We just sent you OTP, check otp.txt for the code')
    code = input('OTP code: ')

    with open('otp.txt', 'r') as f:
        otp = f.read()
    
    if code == otp:
        return True
    else:
        return False
    
# Main program
def main():
    print('Protect My File')
    OTP()
    if input_otp() == False:
        return

    filepath = input('File address (ex: /folder/file.txt): ')

    with open(filepath, 'r') as f:
        data = f.read()

    if data == '':
            print('This file is empty')
            return

    print('--------------------------------')
    print('1. Encrypt')
    print('2. Decrypt')
    print('--------------------------------')
    choice = input('Choice: ')

    # Invalid choice
    while choice > '2' and choice < '1':
        choice = input('Invalid input. New choice: ')

    # Input password
    flag = pass_input(choice)

    if flag == -1:
        return

    if choice == '1':
        encrypt(filepath)
    else:
        decrypt(filepath)


if __name__ == '__main__':
    main()