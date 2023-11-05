from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['your_database_name']

pipeline = [
    {
        "$lookup": {
            "from": "purchase_orders",
            "localField": "customer_id",
            "foreignField": "customer_id",
            "as": "purchase_orders"
        }
    },
    {
        "$unwind": {
            "path": "$purchase_orders",
            "preserveNullAndEmptyArrays": True
        }
    },
    {
        "$lookup": {
            "from": "shipment_details",
            "localField": "purchase_orders.purchase_order_id",
            "foreignField": "purchase_order_id",
            "as": "purchase_orders.shipment_details"
        }
    },
    {
        "$unwind": {
            "path": "$purchase_orders.shipment_details",
            "preserveNullAndEmptyArrays": True
        }
    },
    {
        "$lookup": {
            "from": "purchase_order_details",
            "localField": "purchase_orders.purchase_order_id",
            "foreignField": "purchase_order_id",
            "as": "purchase_orders.purchase_order_details"
        }
    },
    {
        "$group": {
            "_id": "$customer_id",
            "customer": {
                "$first": "$$ROOT"
            }
        }
    },
    {
        "$replaceRoot": {
            "newRoot": "$customer"
        }
    }
]

result = list(db.customers.aggregate(pipeline))

for customer in result:
    print(customer)
