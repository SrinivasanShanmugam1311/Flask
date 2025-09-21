from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "replace-me"

def compute_sip(monthly, annual_rate_pct, years):
    """
    Future value of a monthly SIP with monthly compounding:
      FV = P * [((1+r)^n - 1) / r] * (1+r)
      where r = annual_rate/12, n = years*12
    """
    if monthly <= 0 or annual_rate_pct < 0 or years <= 0:
        return None

    r = (annual_rate_pct / 100.0) / 12.0
    n = int(years * 12)

    if r == 0:
        fv = monthly * n  # no interest case
    else:
        fv = monthly * (((1 + r) ** n - 1) / r) * (1 + r)

    invested = monthly * n
    gain = fv - invested
    return {
        "monthly": monthly,
        "rate": annual_rate_pct,
        "years": years,
        "months": n,
        "invested": round(invested, 2),
        "future_value": round(fv, 2),
        "gain": round(gain, 2),
    }

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/sip", methods=["GET", "POST"])
def sip():
    result = None
    if request.method == "POST":
        try:
            monthly = float(request.form.get("monthly", "0"))
            rate = float(request.form.get("rate", "0"))
            years = float(request.form.get("years", "0"))
        except ValueError:
            flash("Please enter valid numbers.")
            return redirect(url_for("index"))

        result = compute_sip(monthly, rate, years)
        if result is None:
            flash("Monthly>0, Years>0, Rate≥0 are required.")
            return redirect(url_for("index"))

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
