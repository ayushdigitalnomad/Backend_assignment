from flask import Flask, request, jsonify
import uuid

app = Flask(__name)
customers = {}
purchase_orders = {}
purchase_order_details = {}

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

# API to add purchase order details
@app.route('/add_purchase_order_details', methods=['POST'])
def add_purchase_order_details():
    data = request.get_json()
    purchase_order_details_id = str(uuid.uuid4())
    if 'purchase_order_id' in data:
        if data['purchase_order_id'] in purchase_orders:
            data['purchase_order_details_id'] = purchase_order_details_id
            purchase_order_details[purchase_order_details_id] = data

            return jsonify({"message": "Purchase Order Details added successfully", "purchase_order_details_id": purchase_order_details_id})
        else:
            return jsonify({"error": "Purchase Order not found"}, 404)
    else:
        return jsonify({"error": "Missing purchase order details"}, 400)

@app.route('/get_customers_with_purchase_orders', methods=['GET'])
def get_customers_with_purchase_orders():
    customers_with_purchase_orders = []

    for customer_id, customer in customers.items():
        customer_with_orders = customer.copy()
        customer_with_orders['purchase_orders'] = []

        for purchase_order_id, purchase_order in purchase_orders.items():
            if purchase_order['customer_id'] == customer_id:
                purchase_order_with_details = purchase_order.copy()
                purchase_order_with_details['purchase_order_details'] = []

                for purchase_order_details_id, details in purchase_order_details.items():
                    if details['purchase_order_id'] == purchase_order_id:
                        purchase_order_with_details['purchase_order_details'].append(details)

                customer_with_orders['purchase_orders'].append(purchase_order_with_details)

        customers_with_purchase_orders.append(customer_with_orders)

    return jsonify(customers_with_purchase_orders)
if __name__ == '__main__':
    app.run(debug=True)
