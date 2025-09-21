from datetime import date, datetime
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
# app.secret_key = "replace-me"

def compute_age(dob: date):
    today = date.today()
    y = today.year - dob.year
    print(y)
    return y

@app.route("/age", methods=["GET", "POST"])
def calculate():
    age=None
    if request.method == 'POST':
        dob_str = request.form.get('dob')
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()

        result = compute_age(dob)
        if result is None:
            flash("Date of birth cannot be in the future.")
            return redirect(url_for("index"))

        age = result
    return render_template("index.html", age=age)

if __name__ == "__main__":
    app.run(debug=True)