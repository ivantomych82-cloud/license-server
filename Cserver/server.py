from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route("/")
def home():
    return "LICENSE SERVER WORKING"

@app.route("/check", methods=["POST"])
def check():

    data = request.json

    key = data["key"]
    hwid = data["hwid"]

    with open("licenses.json", "r") as f:
        licenses = json.load(f)

    if key not in licenses:
        return jsonify({"status": "invalid"})

    lic = licenses[key]

    if not lic["active"]:
        return jsonify({"status": "disabled"})

    if lic["hwid"] == "":
        lic["hwid"] = hwid

        with open("licenses.json", "w") as f:
            json.dump(licenses, f, indent=4)

    elif lic["hwid"] != hwid:
        return jsonify({"status": "wrong_pc"})

    return jsonify({"status": "ok"})

app.run(host="0.0.0.0", port=5000)