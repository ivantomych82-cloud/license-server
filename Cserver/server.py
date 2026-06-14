from flask import Flask, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "LICENSE SERVER WORKING"

@app.route("/check", methods=["POST"])
def check():

    data = request.json

    key = data["key"]
    hwid = data["hwid"]

    print(f"[CHECK] key={key} hwid={hwid}", flush=True)

    with open("licenses.json", "r") as f:
        licenses = json.load(f)

    if key not in licenses:
        return jsonify({"status": "invalid"})

    lic = licenses[key]

    if not lic["active"]:
        return jsonify({"status": "disabled"})
    
    expire_date = datetime.strptime(
        lic["expires"],
        "%Y-%m-%d"
    )

    if datetime.now() > expire_date:
        return jsonify({"status": "expired"})

    if lic["hwid"] == "":
        lic["hwid"] = hwid

        print(f"[ACTIVATION] {key} -> {hwid}")

        with open("licenses.json", "w") as f:
            json.dump(licenses, f, indent=4)

    elif lic["hwid"] != hwid:
        return jsonify({"status": "wrong_pc"})

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )