from flask import Flask, request, jsonify
import json

app = Flask(__name__)
TOKENS_DB = {}  # ⚠️ TEMP STORAGE — replace with Firebase, Redis, etc.


@app.route('/register-token', methods=['POST'])
def register_token():
    data = request.get_json()
    token = data.get("token")
    if not token:
        return jsonify({"error": "Missing token"}), 400

    # Store or update token (demo only — use DB in real app)
    TOKENS_DB["user123"] = token
    print("✅ Received and stored token:", token)
    return jsonify({"status": "success"}), 200


@app.route('/trigger-alert', methods=['POST'])
def trigger_alert():
    token = TOKENS_DB.get("user123")
    if not token:
        return jsonify({"error": "No token registered"}), 400

    # Send notification using Expo push API
    from requests import post

    message = {
        "to": token,
        "sound": "default",
        "title": "🚨 Sensor Alert",
        "body": "Temperature dropped below 60°F!",
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    response = post("https://exp.host/--/api/v2/push/send",
                    json=message, headers=headers)
    return jsonify(response.json())
