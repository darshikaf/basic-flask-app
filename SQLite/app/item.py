from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required

import sqlite3

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="price is a required field."
    )

    # @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        else:
            return {'message': f'{name} does not exist.'}

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        get_query = "SELECT * FROM item where name=?"
        result = cursor.execute(get_query, (name,))
        item = result.fetchone()
        connection.close()

        if item:
            return {'item': {'name': item[0], 'price': item[1]}}

    def post(self, name):
        if Item.find_by_name(name):
            return {'message': f'An item with name {name} already exists.'}

        request_data = Item.parser.parse_args()
        item = {'name': name, 'price': request_data['price']}
        
        try:
            self.insert(item)
        except:
            return Exception, 500

        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        insert_query = "INSERT INTO item VALUES (?, ?)"
        cursor.execute(insert_query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def delete(self, name):
        item = self.find_by_name(name)
        if not item:
            return {'message': f'Item with name {name} does not exist.'}

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        delete_query = "DELETE FROM item WHERE name=?"
        cursor.execute(delete_query, (name,))

        connection.commit()
        connection.close()

        return ({"message": f"{name} is deleted from items list."})

    def put(self, name):
        request_data = Item.parser.parse_args()

        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': request_data['price']}

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return Exception, 500
        else:
            try:
                self.update(updated_item)
            except:
                return Exception, 500
        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        update_query = "UPDATE item SET price=? WHERE name=?"
        cursor.execute(update_query, (item['price'], item['name'])), 201

        connection.commit()
        connection.close()        


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM item"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        connection.close()
        return {'items': items}

