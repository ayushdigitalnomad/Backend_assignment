from flask import Flask, request, jsonify
import uuid
app = Flask(__name)
customers = {}
purchase_orders = {}

@app.route('/add_customer', methods=['POST'])
def add_customer():
    data = request.get_json()
    customer_id = str(uuid.uuid4())

    customers[customer_id] = data
    customers[customer_id]['customer_id'] = customer_id

    return jsonify({"message": "Customer added successfully", "customer_id": customer_id})

@app.route('/add_purchase_order', methods=['POST'])
def add_purchase_order():
    data = request.get_json()
    purchase_order_id = str(uuid.uuid4())
    data['purchase_order_id'] = purchase_order_id
    purchase_orders[purchase_order_id] = data

    return jsonify({"message": "Purchase Order added successfully", "purchase_order_id": purchase_order_id})

# API to retrieve a customer by customer_id
@app.route('/get_customer/<string:customer_id>', methods=['GET'])
def get_customer(customer_id):
    if customer_id in customers:
        return jsonify(customers[customer_id])
    else:
        return jsonify({"error": "Customer not found"}, 404)
@app.route('/get_purchase_order/<string:purchase_order_id>', methods=['GET'])
def get_purchase_order(purchase_order_id):
    if purchase_order_id in purchase_orders:
        return jsonify(purchase_orders[purchase_order_id])
    else:
        return jsonify({"error": "Purchase Order not found"}, 404)

if __name__ == '__main__':
    app.run(debug=True)
