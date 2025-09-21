from flask import Flask, render_template, request

app = Flask(__name__)

def bmi_category(bmi):
    if bmi < 16: return "Severe Thinness"
    if bmi < 17: return "Moderate Thinness"
    if bmi < 18.5: return "Mild Thinness"
    if bmi < 25: return "Normal"
    if bmi < 30: return "Overweight"
    if bmi < 35: return "Obese Class I"
    if bmi < 40: return "Obese Class II"
    return "Obese Class III"

@app.route("/bmi", methods=["GET","POST"])
def index():
    result = None
    if request.method == "POST":
        weight = float(request.form["weight"])
        height_cm = float(request.form["height"])
        height_m = height_cm / 100
        bmi = round(weight / (height_m ** 2), 2)
        category = bmi_category(bmi)

        # Jina-format dictionary
        result = {
                "bmi": bmi,
                "category": category
            }
    return render_template("bmi.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)