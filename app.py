from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime, timezone

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["github_events"]
collection = db["events"]

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "Flask is running"
    }), 200

from datetime import datetime, timezone

@app.route("/webhook", methods=["POST"])
def github_webhook():

    if request.headers.get("Content-Type") != "application/json":
        return jsonify({"message": "Invalid content type"}), 400

    data = request.get_json()
    event_type = request.headers.get("X-GitHub-Event")

    if event_type == "push":
        document = {
            "request_id": data["head_commit"]["id"],
            "author": data["pusher"]["name"],
            "action": "push",
            "from_branch": None,
            "to_branch": data["ref"].split("/")[-1],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    elif event_type == "pull_request":

        pr = data["pull_request"]

        # MERGE EVENT
        if data["action"] == "closed" and pr.get("merged"):
            document = {
                "request_id": pr["id"],
                "author": pr["user"]["login"],
                "action": "merge",
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        # NORMAL PR EVENT
        else:
            document = {
                "request_id": pr["id"],
                "author": pr["user"]["login"],
                "action": "pull_request",
                "from_branch": pr["head"]["ref"],
                "to_branch": pr["base"]["ref"],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

    else:
        return jsonify({"message": "Event ignored"}), 200

    collection.insert_one(document)

    return jsonify({"message": "Webhook received"}), 200

@app.route("/events", methods=["GET"])
def get_events():
    events = list(collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(100))
    return jsonify(events)

@app.route("/")
def home():
    return render_template("index.html")

#########################################################################

if __name__ == "__main__":    app.run(debug=True, port=5000)