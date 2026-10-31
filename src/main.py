# Expenses Manager – simple Flask API

from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# In‑memory store for demo purposes (not persistent)
expenses = []

@app.route('/api/expense', methods=['POST'])
def create_expense():
    data = request.get_json()
    if not data or 'amount' not in data or 'description' not in data:
        return jsonify({'error': 'Invalid payload'}), 400
    expense = {
        'id': len(expenses) + 1,
        'amount': data['amount'],
        'description': data['description'],
        'timestamp': data.get('timestamp') or ''
    }
    expenses.append(expense)
    return jsonify(expense), 201

@app.route('/api/expense', methods=['GET'])
def list_expenses():
    return jsonify(expenses)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
