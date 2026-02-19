from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)

# ---------------------------
# MongoDB Configuration
# ---------------------------
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI not found in .env file")

client = MongoClient(MONGO_URI)

# Explicitly select database
db = client["test"]
collection = db["users"]

# ---------------------------
# 1. API Route (Reads backend file)
# ---------------------------
@app.route("/api")
def api():
    try:
        users = list(collection.find({}, {"_id": 0}))
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# ---------------------------
# 2. Form Route (Insert into MongoDB)
# ---------------------------
@app.route("/", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")

        try:
            # Validation
            if not name or not email:
                raise ValueError("Name and Email are required")

            # Insert into MongoDB Atlas
            collection.insert_one({
                "name": name,
                "email": email
            })

            # Redirect on success
            return redirect(url_for("success"))

        except Exception as e:
            # Show error on same page (NO redirect)
            return render_template(
                "form.html",
                error=str(e),
                name=name,
                email=email
            )

    return render_template("form.html")


# ---------------------------
# 3. Success Page
# ---------------------------
@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
