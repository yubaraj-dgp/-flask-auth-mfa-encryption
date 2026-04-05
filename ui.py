import tkinter as tk
from tkinter import messagebox

from auth import login
from mfa import generate_otp, verify_otp
from cipher import encrypt, decrypt

# Global variable to store OTP
current_otp = None

# ------------------ FUNCTIONS ------------------ #

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()


# -------- LOGIN SCREEN -------- #
def show_login():
    clear_screen()

    tk.Label(root, text="Login", font=("Arial", 16)).pack(pady=10)

    tk.Label(root, text="Username").pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    def handle_login():
        global current_otp

        username = username_entry.get()
        password = password_entry.get()

        if login(username, password):
            messagebox.showinfo("Success", "Login Successful")

            current_otp = generate_otp()
            print("Your OTP is:", current_otp)  # simulate sending OTP

            show_otp()
        else:
            messagebox.showerror("Error", "Invalid Username or Password")

    tk.Button(root, text="Login", command=handle_login).pack(pady=10)


# -------- OTP SCREEN -------- #
def show_otp():
    clear_screen()

    tk.Label(root, text="MFA Verification", font=("Arial", 16)).pack(pady=10)

    tk.Label(root, text="Enter OTP").pack()
    otp_entry = tk.Entry(root)
    otp_entry.pack()

    def handle_otp():
        try:
            user_otp = int(otp_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Enter valid numeric OTP")
            return

        if verify_otp(current_otp, user_otp):
            messagebox.showinfo("Success", "MFA Verified")
            show_dashboard()
        else:
            messagebox.showerror("Error", "Incorrect OTP")

    tk.Button(root, text="Verify", command=handle_otp).pack(pady=10)


# -------- ENCRYPTION DASHBOARD -------- #
def show_dashboard():
    clear_screen()

    tk.Label(root, text="Encryption Dashboard", font=("Arial", 16)).pack(pady=10)

    tk.Label(root, text="Message").pack()
    msg_entry = tk.Entry(root, width=30)
    msg_entry.pack()

    tk.Label(root, text="Shift Key").pack()
    shift_entry = tk.Entry(root)
    shift_entry.pack()

    def do_encrypt():
        try:
            shift = int(shift_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Shift must be a number")
            return

        msg = msg_entry.get()
        result = encrypt(msg.upper(), shift)
        print("Encrypted Message:", result)

    def do_decrypt():
        try:
            shift = int(shift_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Shift must be a number")
            return

        msg = msg_entry.get()
        result = decrypt(msg.upper(), shift)
        messagebox.showinfo("Decrypted Text", result)

    tk.Button(root, text="Encrypt", command=do_encrypt).pack(pady=5)
    tk.Button(root, text="Decrypt", command=do_decrypt).pack(pady=5)
    tk.Button(root, text="Logout", command=show_login).pack(pady=10)


# ------------------ MAIN WINDOW ------------------ #

root = tk.Tk()
root.title("Secure App with MFA")
root.geometry("350x350")

show_login()

root.mainloop()