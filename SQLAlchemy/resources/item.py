from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required

from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="price is a required field."
    )
    parser.add_argument(
        'store_id',
        type=int,
        required=True,
        help="An item should be associated to a store."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'message': f'{name} does not exist.'}

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name {name} already exists.'}

        request_data = Item.parser.parse_args()
        item = ItemModel(name, request_data['price'], request_data['store_id']) # item = ItemModel(**request_data)
        
        try:
            ItemModel.save_to_db(item)
        except:
            return Exception, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return ({"message": f"{name} is deleted from items list."})

        return {'message': f'Item with name {name} does not exist.'}

    def put(self, name):
        request_data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, request_data['price'], request_data['store_id'])
        else:
            item.price = request_data['price']
        
        item.save_to_db()

        return item.json()       


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}

