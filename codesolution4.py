from flask import Flask, request, jsonify
import uuid

app = Flask(__name)

customers = {}
purchase_orders = {}
shipping_details = {}
shipment_details = {}

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

    # Generate a unique Purchase Order ID using uuid
    purchase_order_id = str(uuid.uuid4())

    data['purchase_order_id'] = purchase_order_id
    purchase_orders[purchase_order_id] = data

    return jsonify({"message": "Purchase Order added successfully", "purchase_order_id": purchase_order_id})

# API to add shipping details
@app.route('/add_shipping_details', methods=['POST'])
def add_shipping_details():
    data = request.get_json()

    # Generate a unique Shipping Details ID using uuid
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

# API to add shipment details
@app.route('/add_shipment_details', methods=['POST'])
def add_shipment_details():
    data = request.get_json()
    shipment_details_id = str(uuid.uuid4())

    shipment_details[shipment_details_id] = data

    return jsonify({"message": "Shipment Details added successfully", "shipment_details_id": shipment_details_id})
@app.route('/get_customers_by_city/<string:city>', methods=['GET'])
def get_customers_by_city(city):
    matching_customers = []
    for customer_id, customer in customers.items():
        if 'customer_id' in customer and 'city' in customer and customer['city'] == city:
            matching_customers.append(customer)
    return jsonify(matching_customers)
if __name__ == '__main__':
    app.run(debug=True)
