from flask import Flask, request, jsonify
import uuid

app = Flask(__name)

# Create an empty dictionary to store customer data
customers = {}


# API to add a customer
@app.route('/add_customer', methods=['POST'])
def add_customer():
    data = request.get_json()

    # Generate a unique Customer ID using uuid
    customer_id = str(uuid.uuid4())

    # Validate the input data
    if 'customer_name' in data and 'email' in data and 'mobile_number' in data and 'city' in data:
        customers[customer_id] = {
            'customer_id': customer_id,
            'customer_name': data['customer_name'],
            'email': data['email'],
            'mobile_number': data['mobile_number'],
            'city': data['city']
        }
        return jsonify({"message": "Customer added successfully", "customer_id": customer_id})
    else:
        return jsonify({"error": "Missing customer details"}, 400)


# API to retrieve customer details by customer_id
@app.route('/get_customer/<string:customer_id>', methods=['GET'])
def get_customer(customer_id):
    if customer_id in customers:
        return jsonify(customers[customer_id])
    else:
        return jsonify({"error": "Customer not found"}, 404)


if __name__ == '__main__':
    app.run(debug=True)