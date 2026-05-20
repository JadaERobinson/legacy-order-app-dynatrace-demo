from flask import Flask, jsonify, request
import sqlite3
import time
import random

app = Flask(__name__)

@app.route("/billing/<id>")
def get_billing(id):
    demo = request.args.get('demo', '').lower()

    # Simulate slow legacy DB
    time.sleep(1.5)
    if random.random() < 0.3:
        time.sleep(2)

    if demo == 'slow':
        time.sleep(3)
    if demo == 'error':
        return jsonify({
            'customerId': id,
            'service': 'billing',
            'error': 'Intentional billing service error triggered for demo'
        }), 500

    conn = sqlite3.connect('billing.db')
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM billing WHERE customer_id=?", (id,))
    result = cursor.fetchone()
    conn.close()

    balance = result[0] if result else 0

    return jsonify({
        "customerId": id,
        "balance": balance,
        "service": "billing"
    })

app.run(host="0.0.0.0", port=5001)
