from flask import Flask, jsonify
import cloudscraper
import time

app = Flask(__name__)

# Cloudflare bypass client
scraper = cloudscraper.create_scraper()

# Current session cache
current_session = {
    "address": None,
    "session_url": "https://10minutemail.com/session/address"
}

@app.route("/get-email", methods=["GET"])
def get_email():
    """
    Return the current 10MinuteMail session email
    """
    try:
        response = scraper.get(current_session["session_url"], timeout=10)
        data = response.json()
        email = data.get("address")
        current_session["address"] = email
        return jsonify({
            "success": True if email else False,
            "data": {"address": email}
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/refresh-email", methods=["GET"])
def refresh_email():
    """
    Generate a new 10MinuteMail session (new email)
    """
    try:
        # Trigger new session
        scraper.get("https://10minutemail.com/session/new", timeout=10)

        # Sometimes session needs a tiny delay to register
        time.sleep(0.5)

        # Get the new email
        response = scraper.get(current_session["session_url"], timeout=10)
        data = response.json()
        email = data.get("address")
        current_session["address"] = email

        return jsonify({
            "success": True if email else False,
            "data": {"address": email}
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/")
def home():
    return "API Running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
