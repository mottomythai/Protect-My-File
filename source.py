# Yeu cau: obfuscated code

def hash():
    return none 

# Hash password va kiem tra voi hash duoc luu
def pass_input(choice):
    key = input("Nhap key ma hoa: ", end="")

    if choice == '1':
        # Save the new key
        print("h")

    if choice == '2':
        # Check if the key is matching
        print("b")

    return key

# Kiem tra mat khau "dong"
def OTP():
    return True

def enc_dec(password, choice):
    return

def main():
    # Chuong trinh ma hoa
    print("Chuong trinh ma hoa/giai ma file")
    f_address = input("Nhap dia chi file ", end="")
    print("--------------------------------")
    print("1. Ma hoa file")
    print("2. Giai ma file")
    print("--------------------------------")
    choice = input("Ban chon: ", end="")

    # Neu nhu choice khong phu hop 
    while choice > '2' and choice < '1':
        choice = input("Lua chon khong hop le. Nhap lai: ", end="")

    # Nhap password
    password = pass_input(choice)

    # Nhap mat khau "dong"
    if OTP():
        # Ma hoa/giai ma file
        enc_dec(password, choice)

    
    

    

if __name__ == "__main__":
    main()