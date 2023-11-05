from flask import Flask, request, jsonify
import uuid

app = Flask(__name)

customers = {}
purchase_orders = {}
shipping_details = {}

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

@app.route('/add_shipping_details', methods=['POST'])
def add_shipping_details():
    data = request.get_json()

    shipping_details_id = str(uuid.uuid4())

    if 'purchase_order_id' in data and 'customer_id' in data:
        if data['purchase_order_id'] in purchase_orders and data['customer_id'] in customers:
            data['shipping_details_id'] = shipping_details_id
            shipping_details[shipping_details_id] = data

            return jsonify({"message": "Shipping Details added successfully", "shipping_details_id": shipping_details_id})
        else:
            return jsonify({"error": "Purchase Order or Customer not found"}, 404)
    else:
        return jsonify({"error": "Missing shipping details"}, 400)

if __name__ == '__main__':
    app.run(debug=True)
