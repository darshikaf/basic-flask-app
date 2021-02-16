from flask import Flask,jsonify, request
import json

app = Flask(__name__)


stores = [
    {
        "name": "storea",
        "items": [
            {
                "name": "item1",
                "price": "15.99"
            }
        ]
    },
    {
        "name": "storeb",
        "items": [
            {
                "name": "item2",
                "price": "18.99"
            }
        ]
    }
]

# sanity check
@app.route("/")
def home_page():
    return "<h1>Store catalogue</h1>"

# POST /store data: {name:}
@app.route("/store", methods=['POST'])
def create_store():
    request_data = request.get_json()
    print(type(request_data))
    new_store = {
        "name": request_data["name"],
        "items": []
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET /stores 
@app.route("/stores")
def get_stores():
    return jsonify({'stores': stores})

# GET /store/<string:name>
@app.route("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': f'{name} not found'})

# GET /store/<string:name>/item
@app.route("/store/<string:name>/item")
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': f'{name} not found'})

# POST /store/<string:name>/item {name:, price:}
@app.route("/store/<string:name>/item", methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
           new_item = {
                "name": request_data['name'],
                "price": request_data['price']
           }
           store['items'].append(new_item)
           return jsonify(new_item)
    return ({'message': f'{name} is not a store.'})

# POST /store/<string:name>/location {location:}
@app.route("/store/<string:name>/location", methods=['POST'])
def create_location(name):
    for store in stores:
        if store["name"] == name:
            request_data = request.get_json()
            store["location"] = request_data["location"]
            return jsonify(store)
    return ({"message": f"{name} is not a store."})


app.run(port=5000, debug=True)