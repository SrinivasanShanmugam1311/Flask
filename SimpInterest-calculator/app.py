from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "replace-me"

def compute_simple_interest(p, r_pct, t_years):
    # SI = P * R * T / 100 ; Amount = P + SI
    if p <= 0 or r_pct < 0 or t_years <= 0:
        return None
    si = p * r_pct * t_years / 100.0
    amount = p + si
    return {
        "principal": round(p, 2),
        "rate": r_pct,
        "years": t_years,
        "simple_interest": round(si, 2),
        "amount": round(amount, 2),
    }

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/si", methods=["GET","POST"])
def si():
    result = None
    if request.method == "POST":
        try:
            p = float(request.form.get("principal","0"))
            r = float(request.form.get("rate","0"))
            t = float(request.form.get("years","0"))
        except ValueError:
            flash("Please enter valid numbers.")
            return redirect(url_for("index"))

        result = compute_simple_interest(p, r, t)
        if result is None:
            flash("Principal>0, Years>0, Rate≥0 are required.")
            return redirect(url_for("index"))

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
