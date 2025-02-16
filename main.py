from flask import Flask, request, render_template
import re
app = Flask(__name__)
def check_password_strength(password):
    length_criteria = len(password) >= 8
    upper_criteria = re.search(r"[A-Z]", password) is not None
    lower_criteria = re.search(r"[a-z]", password) is not None
    digit_criteria = re.search(r"\d", password) is not None
    special_criteria = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is not None
    score = sum([length_criteria, upper_criteria, lower_criteria, digit_criteria, special_criteria])
    if score == 5:
        strength = "Strong"
        color = "green"
    elif score >= 3:
        strength = "Medium"
        color = "orange"
    else:
        strength = "Weak"
        color = "red"
    return strength, color, {
        "Length (8+ chars)": "✅" if length_criteria else "❌",
        "Uppercase Letter": "✅" if upper_criteria else "❌",
        "Lowercase Letter": "✅" if lower_criteria else "❌",
        "Digit (0-9)": "✅" if digit_criteria else "❌",
        "Special Character": "✅" if special_criteria else "❌"
    }
@app.route('/', methods=['GET', 'POST'])
def home():
    result, color, criteria = None, None, {}
    if request.method == 'POST':
        password = request.form.get("password", "")
        if password:
            result, color, criteria = check_password_strength(password)
    return render_template("index.html", result=result, color=color, criteria=criteria)
if __name__ == '__main__':
    app.run(debug=True)
