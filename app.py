from flask import Flask, render_template, request, redirect, session
from auth import login
from mfa import generate_otp, verify_otp
from cipher import encrypt, decrypt

app = Flask(__name__)
app.secret_key = "secret123"  # required for session

current_otp = None


# -------- LOGIN -------- #
@app.route("/", methods=["GET", "POST"])
def login_page():
    global current_otp

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if login(username, password):
            current_otp = generate_otp()
            print("OTP:", current_otp)

            return redirect("/otp")
        else:
            return "Invalid Login"

    return render_template("login.html")


# -------- OTP -------- #
@app.route("/otp", methods=["GET", "POST"])
def otp_page():
    global current_otp

    if request.method == "POST":
        user_otp = int(request.form["otp"])

        if verify_otp(current_otp, user_otp):
            session["logged_in"] = True
            return redirect("/dashboard")
        else:
            return "Wrong OTP"

    return render_template("otp.html")


# -------- DASHBOARD -------- #
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if not session.get("logged_in"):
        return redirect("/")

    result = ""

    if request.method == "POST":
        msg = request.form["message"]
        shift = int(request.form["shift"])

        if "encrypt" in request.form:
            result = encrypt(msg.upper(), shift)
        elif "decrypt" in request.form:
            result = decrypt(msg.upper(), shift)

    return render_template("dashboard.html", result=result)


# -------- LOGOUT -------- #
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)