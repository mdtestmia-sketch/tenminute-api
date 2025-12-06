from flask import Flask, jsonify
import cloudscraper
import re

app = Flask(__name__)

# Cloudflare bypass client
scraper = cloudscraper.create_scraper()

# Cache for current email session
current_session = {
    "address": None,
    "session_url": "https://10minutemail.com/session/address"
}

def extract_email_from_html(html_text):
    """
    Extract email address from 10MinuteMail HTML response using regex
    """
    match = re.search(r'"address":"([A-Za-z0-9@.]*)"', html_text)
    if match:
        return match.group(1)
    return None

@app.route("/get-email", methods=["GET"])
def get_email():
    """
    Return the current session email address
    """
    try:
        response = scraper.get(current_session["session_url"])
        html_text = response.text
        email = extract_email_from_html(html_text)
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
        scraper.get("https://10minutemail.com/session/new")

        # Get current email address
        response = scraper.get("https://10minutemail.com/session/address")
        html_text = response.text
        email = extract_email_from_html(html_text)
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
