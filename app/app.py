from flask import Flask, request, jsonify
from flask import render_template, flash, redirect
import json
import util

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("app.html")


@app.route("/predict_home_price", methods=["GET", "POST"])
def predict_home_price():
    city = request.form["city"]
    district = request.form["district"]
    total_sqft = float(request.form["total_sqft"])
    lot_size = float(request.form["lot_size"])
    bedrooms = int(request.form["bedrooms"])
    bathrooms = int(request.form["bathrooms"])
    yr_built = int(request.form["yr_built"])
    garage = int(request.form["garage"])
    response = jsonify(
        {
            "estimated_price": util.predict_price(
                city,
                district,
                total_sqft,
                lot_size,
                bedrooms,
                bathrooms,
                yr_built,
                garage,
            )
        }
    )
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=5000)
