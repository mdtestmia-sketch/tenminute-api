from flask import Flask, jsonify
import cloudscraper

app = Flask(__name__)
scraper = cloudscraper.create_scraper()

@app.route("/get-email", methods=["GET"])
def get_email():
    try:
        url = "https://10minutemail.com/session/address"
        response = scraper.get(url)
        return jsonify({
            "success": True,
            "data": response.text
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route("/")
def home():
    return "API Running on Railway!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
