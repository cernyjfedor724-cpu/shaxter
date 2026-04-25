from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

LEADERBOARD_FILE = "leaderboard.json"

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    return []

def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/api/top", methods=["GET"])
def get_top():
    data = load_leaderboard()
    data.sort(key=lambda x: x.get("total_ore", 0), reverse=True)
    return jsonify(data[:10])

@app.route("/api/update", methods=["POST"])
def update_score():
    body = request.get_json()
    if not body or not body.get("user_id"):
        return jsonify({"error": "invalid data"}), 400

    user_id = str(body["user_id"])
    total_ore = int(body.get("total_ore", 0))

    leaderboard = load_leaderboard()
    player = next((p for p in leaderboard if p["user_id"] == user_id), None)
    if player is None:
        player = {"user_id": user_id, "total_ore": 0}
        leaderboard.append(player)

    if total_ore > player["total_ore"]:
        player["total_ore"] = total_ore

    save_leaderboard(leaderboard)
    return jsonify({"status": "ok", "total_ore": player["total_ore"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
