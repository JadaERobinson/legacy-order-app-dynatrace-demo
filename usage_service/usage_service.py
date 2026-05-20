from flask import Flask, jsonify
import sqlite3
import time

app = Flask(__name__)

@app.route("/usage/<id>")
def get_usage(id):
    time.sleep(0.3)  # faster than billing

    conn = sqlite3.connect('usage.db')
    cursor = conn.cursor()
    cursor.execute("SELECT data_usage FROM usage WHERE customer_id=?", (id,))
    result = cursor.fetchone()
    conn.close()

    usage = result[0] if result else 0

    return jsonify({
        "customerId": id,
        "usage": usage,
        "service": "usage"
    })

app.run(host="0.0.0.0", port=5002)