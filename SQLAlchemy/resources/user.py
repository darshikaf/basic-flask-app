from flask_restful import Resource, Api, reqparse
import sqlite3

from models.user import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username",
        type=str,
        required=True,
        help="username is a required field.",
    )
    parser.add_argument(
        "password",
        type=str,
        required=True,
        help="password is a required field.",
    )

    def post(self):
        request_data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(request_data['username']):
            return {'message': 'Username already exists'}, 400

        user = UserModel(**request_data) #unpacked as (request_data[0], request_data[1])
        user.save_to_db()

        return {"message": "User registered successfully."}, 201
