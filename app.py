from flask import Flask, request, jsonify, send_from_directory
import os
import sqlite3

app = Flask(__name__, static_folder="static")

DB_PATH = "vault.db"
PASSWORD = os.environ.get("VAULT_PASSWORD")
NEXT_URL = os.environ.get("NEXT_CHALLENGE_URL")

# Create DB with password hash
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS vault (id INTEGER PRIMARY KEY, password TEXT)")
    c.execute("DELETE FROM vault")
    c.execute("INSERT INTO vault (password) VALUES (?)", (PASSWORD,))
    conn.commit()
    conn.close()

@app.route("/api/unlock", methods=["POST"])
def unlock():
    code = request.json.get("code", "")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password FROM vault WHERE password = ?", (code,))
    match = c.fetchone()
    conn.close()

    if match:
        return jsonify(success=True, next=NEXT_URL)
    return jsonify(success=False)

@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
