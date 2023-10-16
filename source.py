# Yeu cau: 

# 3. Obfuscated code

# 5. Check for unsual condition

import random
import string
import hashlib
import time
import cryptography.fernet

# 1. Hash key for min 100 bit
# Hashing
def hashing(password):
    hash = hashlib.md5(password.encode())
    return hash.hexdigest()

# 
def pass_input(choice):
    password = input('Input password: ')

    with open('pass.txt', 'r') as fr:
        storedhash = fr.read()

    newhash = hashing(password)

    if choice == '1':
                
        if storedhash != '':
            ans = input('Password is already stored. Create new password? (y/n) ')
            if ans == 'n' or ans == 'N':
                return

        with open('pass.txt', 'w') as fw:
            fw.write(newhash)

    if choice == '2':
        # Check if the key is matching
        if newhash != storedhash:
            print('Wrong password')
            return

    return password


def add_timestamp(filepath):
    nowtime = time.time()

    with open(filepath, 'a') as f:
        f.write(nowtime)

def del_timestamp(filepath):
    with open(filepath, 'r') as fr:
        mess = fr.read()

    mess = mess[-18:]

    with open(filepath, 'w') as fw:
        fw.write(mess)
     
# 2. Encrypt new version each time
# File encryption/decryption
def encrypt(filepath):
    add_timestamp(filepath)

    with open(filepath, 'rb') as fr:
        data = fr.read()

    with open('pass.txt', 'rb') as fp:
        fernet = cryptography.fernet.Fernet(fp.read())
    
    result = fernet.encrypt(data)

    with open(filepath, 'wb') as fw:
        fw.write(result)

def decrypt(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()

    with open('pass.txt', 'rb') as fp:
        fernet = cryptography.fernet.Fernet(fp.read())
    
    result = fernet.decrypt(data)

    with open(filepath, 'wb') as fw:
        fw.write(result)

    del_timestamp(filepath)

# 4. Required OTP anytime logins
# OTP
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
    

def main():
    # Main program
    print('Protect My File')
    OTP()
    if input_otp() == False:
        return

    filepath = input('File address (ex: /folder/file.txt): ')

    with open(filepath, 'r') as f:
        if f.read() == '':
            print('This file is empty')
            return

    print('--------------------------------')
    print('1. Encrypt')
    print('2. Decrypt')
    print('--------------------------------')
    choice = input('Choice: ')

    # Neu nhu choice khong phu hop 
    while choice > '2' and choice < '1':
        choice = input('Invalid input. New choice: ')

    # Nhap password
    pass_input(choice)

    if choice == 1:
        # Encrypt
        encrypt(filepath)
    else:
        # Decrypt
        decrypt(filepath)


if __name__ == '__main__':
    main()