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
    """
    @api {get} /customer/:customer_id Get Customer by ID
    @apiName GetCustomer
    @apiGroup Customers
    @apiVersion 1.0.0

    @apiParam {Number} customer_id Customer's unique ID.

    @apiSuccess {Number} id Customer's unique ID.
    @apiSuccess {String} name Customer's name.
    @apiSuccess {Number} balance Customer's balance.

    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "id": 1,
            "name": "John Doe",
            "balance": 1500
        }
    """
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM customers WHERE id = ?', (id,))
    customer = cursor.fetchone()
    conn.close()
    if customer:
        return jsonify(dict(customer))
    return jsonify({'message': 'Customer not found'}), 404

@app.route('/transaction/<int:id>', methods=['GET'])
def get_transaction(id):
    """
    @api {get} /transaction/:transaction_id Get Transaction by ID
    @apiName GetTransaction
    @apiGroup Transactions
    @apiVersion 1.0.0

    @apiParam {Number} transaction_id Transaction's unique ID.

    @apiSuccess {Number} id Transaction's unique ID.
    @apiSuccess {String} name Customer's name.
    @apiSuccess {Number} balance Customer's balance.

    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        {
            "id": 1,
            "name": "John Doe",
            "balance": 1500
        }
    """
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM transactions WHERE id = ?', (id,))
    transaction = cursor.fetchone()
    conn.close()
    if transaction:
        return jsonify(dict(transaction))
    return jsonify({'message': 'Transaction not found'}), 404


@app.route('/transactions/<int:customer_id>', methods=['GET'])
def get_transactions_by_customer(customer_id):
    """
    @api {get} /transactions/:customer_id Get Transactions by Customer ID
    @apiName GetTransactionsByCustomer
    @apiGroup Transactions

    @apiParam {Number} customer_id Customer's unique ID.

    @apiSuccess {Object[]} transactions List of transactions for the customer.
    @apiSuccess {Number} transactions.id Transaction's unique ID.
    @apiSuccess {Number} transactions.customer_id Customer's unique ID.
    @apiSuccess {String} transactions.transaction_type Type of transaction (e.g., 'deposit' or 'withdrawal').
    @apiSuccess {Number} transactions.amount Transaction amount.
    @apiSuccess {String} transactions.date Date and time of the transaction.

    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        [
            {
                "id": 1,
                "customer_id": 123,
                "transaction_type": "deposit",
                "amount": 100.0,
                "date": "2023-08-03 12:34:56"
            },
            {
                "id": 2,
                "customer_id": 123,
                "transaction_type": "withdrawal",
                "amount": 50.0,
                "date": "2023-08-04 10:20:30"
            },
            ...
        ]

    @apiErrorExample {json} Error-Response:
        HTTP/1.1 404 Not Found
        {
            "message": "Customer not found"
        }
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the customer exists
    cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
    customer = cursor.fetchone()
    if not customer:
        conn.close()
        return jsonify({'message': 'Customer not found'}), 404

    # Fetch transactions for the customer based on customer_id
    cursor.execute('SELECT * FROM transactions WHERE customer_id = ?', (customer_id,))
    transactions = cursor.fetchall()
    conn.close()

    # Format the response as a list of dictionaries
    result = []
    for transaction in transactions:
        result.append({
            'id': transaction['id'],
            'customer_id': transaction['customer_id'],
            'transaction_type': transaction['transaction_type'],
            'amount': transaction['amount'],
            'date': transaction['date']
        })

    return jsonify(result), 200

@app.route('/atm-locations', methods=['GET'])
def get_atm_locations():
    """
    @api {get} /atm-locations Get ATM Locations
    @apiName GetATMLocations
    @apiGroup ATM Locations
    @apiVersion 1.0.0

    @apiSuccess {Object[]} atm_locations List of ATM locations.
    @apiSuccess {Number} atm_locations.id ATM's unique ID.
    @apiSuccess {Number} atm_locations.latitude Latitude of the ATM location.
    @apiSuccess {Number} atm_locations.longitude Longitude of the ATM location.
    @apiSuccess {String} atm_locations.bank_name Name of the bank associated with the ATM.
    @apiSuccess {String} atm_locations.address Address of the ATM location.

    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 200 OK
        [
            {
                "id": 1,
                "latitude": 33.7490,
                "longitude": -84.3880,
                "bank_name": "Peachtree Plaza",
                "address": "123 Peachtree St NE, Atlanta, GA"
            },
            {
                "id": 2,
                "latitude": 33.7749,
                "longitude": -84.2963,
                "bank_name": "Centennial Park",
                "address": "456 Marietta St NW, Atlanta, GA"
            },
            {
                "id": 3,
                "latitude": 33.7537,
                "longitude": -84.3880,
                "bank_name": "Georgia Aquarium",
                "address": "789 Luckie St NW, Atlanta, GA"
            },
            ...
        ]

    @apiErrorExample {json} Error-Response:
        HTTP/1.1 400 Bad Request
        {
            "message": "Latitude and longitude coordinates are required"
        }

        HTTP/1.1 404 Not Found
        {
            "message": "No ATM locations found for the provided coordinates"
        }
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch ATM locations based on the provided latitude and longitude coordinates
    cursor.execute('SELECT * FROM atm_locations ')
    atm_locations = cursor.fetchall()
    conn.close()

    if not atm_locations:
        return jsonify({'message': 'No ATM locations found for the provided coordinates'}), 404

    # Format the response as a list of dictionaries
    result = []
    for location in atm_locations:
        result.append({
            'id': location['id'],
            'latitude': location['latitude'],
            'longitude': location['longitude'],
            'bank_name': location['bank_name'],
            'address': location['address']
        })

    return jsonify(result), 200

@app.route('/customers', methods=['POST'])
def create_customer():
    """
    @api {post} /customers Make a New Customer
    @apiName NewCustomer
    @apiGroup Customers
    @apiVersion 1.0.0

    @apiParam {String} name Customer's name.
    @apiParam {String} username Customer's login username.
    @apiParam {String} password Customer's login password.
    @apiParam {Number} balance Customer's balance.
    @apiSuccess {String} message New Customer created successfully.

    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 201 Created
        {
            "message": "New Customer created successfully"
        }
    """
    if not request.json or 'name' not in request.json or 'user' not in request.json or 'password' not in request.json or 'balance' not in request.json:
        return jsonify({'message': 'Invalid data'}), 400

    name = request.json['name']
    user = request.json['user']
    password = request.json['password']
    balance = request.json['balance']

    # Hash the password before storing it in the database
    password_hash = password + "_hash"

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the username already exists
    cursor.execute('SELECT * FROM customers WHERE user = ?', (user,))
    existing_user = cursor.fetchone()
    if existing_user:
        conn.close()
        return jsonify({'message': 'Username already exists'}), 409

    # Insert the new customer into the customers table
    cursor.execute('INSERT INTO customers (name, user, password_hash, balance) VALUES (?, ?, ?, ?)',
                   (name, user, password_hash, balance))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Customer created successfully'}), 201


# DEPOSIT
@app.route('/deposit', methods=['POST'])
def deposit():
    """
    @api {post} /deposit Make a Deposit
    @apiName Deposit
    @apiGroup Transactions
    @apiVersion 1.0.0

    @apiParam {Number} customer_id Customer's unique ID.
    @apiParam {Number} amount Amount to deposit.

    @apiSuccess {String} message Deposit successful.

    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 201 Created
        {
            "message": "Deposit successful"
        }
    """
    if not request.json or 'customer_id' not in request.json or 'amount' not in request.json:
        return jsonify({'message': 'Invalid data'}), 400

    customer_id = request.json['customer_id']
    amount = request.json['amount']

    # Check if the customer exists
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
    customer = cursor.fetchone()
    if not customer:
        conn.close()
        return jsonify({'message': 'Customer not found'}), 404

    # Record the deposit transaction
    conn.execute('INSERT INTO deposits (customer_id, amount) VALUES (?, ?)', (customer_id, amount))

    # Update the customer's balance
    new_balance = customer['balance'] + amount
    conn.execute('UPDATE customers SET balance = ? WHERE id = ?', (new_balance, customer_id))

    # Record the transaction in the transactions table
    conn.execute('INSERT INTO transactions (customer_id, transaction_type, amount, new_balance) VALUES (?, ?, ?, ?)',
                 (customer_id, 'deposit', amount, new_balance))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Deposit successful'}), 201

# WITHDRAWAL
@app.route('/withdrawal', methods=['POST'])
def withdrawal():
    """
    @api {post} /withdrawal Make a Withdrawal
    @apiName Withdrawal
    @apiGroup Transactions
    @apiVersion 1.0.0

    @apiParam {Number} customer_id Customer's unique ID.
    @apiParam {Number} amount Amount to withdraw.

    @apiSuccess {String} message Withdrawal successful.

    @apiSuccessExample {json} Success-Response:
        HTTP/1.1 201 Created
        {
            "message": "Withdrawal successful"
        }
    """
    if not request.json or 'customer_id' not in request.json or 'amount' not in request.json:
        return jsonify({'message': 'Invalid data'}), 400
    
    customer_id = request.json['customer_id']
    amount = request.json['amount']

    # Check if the customer exists
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
    customer = cursor.fetchone()
    if not customer:
        conn.close()
        return jsonify({'message': 'Customer not found'}), 404

    # Check if the customer has sufficient balance
    if customer['balance'] < amount:
        conn.close()
        return jsonify({'message': 'Insufficient balance'}), 400

    # Record the withdrawal transaction
    conn.execute('INSERT INTO withdrawals (customer_id, amount) VALUES (?, ?)', (customer_id, amount))

    # Update the customer's balance
    new_balance = customer['balance'] - amount
    conn.execute('UPDATE customers SET balance = ? WHERE id = ?', (new_balance, customer_id))

    # Record the transaction in the transactions table
    conn.execute('INSERT INTO transactions (customer_id, transaction_type, amount, new_balance) VALUES (?, ?, ?, ?)',
                 (customer_id, 'withdrawal', amount, new_balance))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Withdrawal successful'}), 201

if __name__ == '__main__':
    app.run(debug=True)
