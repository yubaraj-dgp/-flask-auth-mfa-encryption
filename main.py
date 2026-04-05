from auth import login
from mfa import generate_otp, verify_otp
from cipher import encrypt, decrypt

# Step 1: Login
username = input("Username: ")
password = input("Password: ")

if not login(username, password):
    print("Invalid login ❌")
    exit()

print("Login successful ✅")

# Step 2: MFA
otp = generate_otp()
print("OTP:", otp)

user_otp = int(input("Enter OTP: "))

if not verify_otp(otp, user_otp):
    print("Wrong OTP ❌")
    exit()

print("MFA verified ✅")

# Step 3: Encryption
msg = input("Enter message: ")
shift = int(input("Enter shift: "))

enc = encrypt(msg.upper(), shift)
print("Encrypted:", enc)

print("Decrypted:", decrypt(enc, shift))