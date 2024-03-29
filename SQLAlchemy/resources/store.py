from flask_restful import Resource
from flask_jwt import JWT, jwt_required

from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json()
        return {'message': f'Store {name} not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {f'Store with name {name} already exists'}, 404
        
        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred creating the store."}, 500
            
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            try:
                store.StoreModel.delete_from_db()
            except:
                return {"message": "An error occurred creating the store."}, 500
                
        return {'message': 'Store deleted.'}

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}