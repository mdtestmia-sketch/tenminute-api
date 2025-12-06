from flask import Flask, jsonify
import cloudscraper

app = Flask(__name__)

# Cloudflare bypass client
scraper = cloudscraper.create_scraper()

# Current session email cache
current_session = {
    "address": None,
    "session_url": "https://10minutemail.com/session/address"
}

@app.route("/get-email", methods=["GET"])
def get_email():
    """
    Return the current session email address
    """
    try:
        response = scraper.get(current_session["session_url"])
        # Update cached email
        current_session["address"] = response.json().get("address")
        return jsonify({
            "success": True,
            "data": {"address": current_session["address"]}
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/refresh-email", methods=["GET"])
def refresh_email():
    """
    Generate a new 10MinuteMail session (new email)
    """
    try:
        # Hit the /session/new endpoint to get a new email session
        new_session_url = "https://10minutemail.com/session/new"
        scraper.get(new_session_url)  # triggers new session
        # Now get the new email address
        response = scraper.get("https://10minutemail.com/session/address")
        current_session["address"] = response.json().get("address")
        return jsonify({
            "success": True,
            "data": {"address": current_session["address"]}
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/")
def home():
    return "API Running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
