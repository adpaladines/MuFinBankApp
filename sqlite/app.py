from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# TO RUN THE ApiDoc Generator, execute in terminal 'npm run apidoc'
# Database connection
def get_db_connection():
    conn = sqlite3.connect('data/banking.db')
    conn.row_factory = sqlite3.Row
    return conn

# API endpoints
# GET Services
@app.route('/customers', methods=['GET'])
def get_customers():
    """
    @api {get} /customers Get All Customers
    @apiName GetCustomers
    @apiGroup Customers
    @apiVersion 1.0.0

    @apiSuccess {Object[]} customers List of customers.
    @apiSuccess {Number} customers.id Customer's unique ID.
    @apiSuccess {String} customers.name Customer's name.
    @apiSuccess {Number} customers.balance Customer's balance.

    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        [
            {
                "id": 1,
                "name": "John Doe",
                "balance": 1500
            },
            {
                "id": 2,
                "name": "Jane Smith",
                "balance": 2000
            }
        ]
    """

    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM customers')
    customers = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in customers])

@app.route('/transactions', methods=['GET'])
def get_transactions():
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in transactions])

@app.route('/customer/<int:id>', methods=['GET'])
def get_customer(id):
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM customers WHERE id = ?', (id,))
    customer = cursor.fetchone()
    conn.close()
    if customer:
        return jsonify(dict(customer))
    return jsonify({'message': 'Customer not found'}), 404

@app.route('/transaction/<int:id>', methods=['GET'])
def get_transaction(id):
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM transactions WHERE id = ?', (id,))
    transaction = cursor.fetchone()
    conn.close()
    if transaction:
        return jsonify(dict(transaction))
    return jsonify({'message': 'Transaction not found'}), 404

# POST Services
@app.route('/customers', methods=['POST'])
def create_customer():
    if not request.json or 'name' not in request.json or 'balance' not in request.json:
        return jsonify({'message': 'Invalid data'}), 400

    name = request.json['name']
    balance = request.json['balance']

    # Insert the new customer into the database
    conn = get_db_connection()
    cursor = conn.execute('INSERT INTO customers (name, balance) VALUES (?, ?)', (name, balance))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Customer created successfully'}), 201



# PUT Services
@app.route('/customer/<int:id>', methods=['PUT'])
def update_customer(id):
    if not request.json or 'balance' not in request.json:
        return jsonify({'message': 'Invalid data'}), 400

    balance = request.json['balance']

    # Update the customer's balance in the database
    conn = get_db_connection()
    cursor = conn.execute('UPDATE customers SET balance = ? WHERE id = ?', (balance, id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Customer balance updated successfully'})


if __name__ == '__main__':
    app.run(debug=True)
