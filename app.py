from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Allow all origins by default

EMAIL = "test.acc@codsol.co"
PASSWORD = "2285268"

def login(email, password):
    url = "https://codsolution.co/ship/Api/loginApi"
    params = {"email": email, "password": password}
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()

def track_parcel(token, tracking_number):
    url = "https://codsolution.co/ship/Api/track_parcel/"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"tracking_number": tracking_number}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def format_tracking_info(tracking_info):
    if not tracking_info:
        return "No tracking updates found."

    output = "\n📦 Shipment Tracking History:\n\n"
    for update in tracking_info:
        date = update.get("date", "")
        time = update.get("time", "")
        status = update.get("Status", "")
        comment = update.get("comment", "")

        output += f"[{date} {time}] - {status}\n"
        if comment:
            output += f"  → {comment}\n"
        output += "-" * 60 + "\n"
    return output.strip()

@app.route("/track", methods=["POST"])
def track():
    data = request.get_json()
    tracking_number = data.get("tracking_number")

    if not tracking_number:
        return jsonify({"error": "Missing tracking_number"}), 400

    try:
        auth = login(EMAIL, PASSWORD)
        token = auth["bearer_token"]
        tracking_info = track_parcel(token, tracking_number)
        formatted_info = format_tracking_info(tracking_info)
        return formatted_info, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
