from flask_restful import Resource, Api, reqparse
import sqlite3


class User:
    def __init__(self, _id, username, password):
        self.username = username
        self.id = _id
        self.password = password

    @classmethod
    def find_by_username(
        cls, username
    ):  # can be written as a classmethod because self is not used anywhere
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        select_query = "SELECT * FROM user WHERE username=?"
        result = cursor.execute(select_query, (username,))
        row = result.fetchone()

        if row:
            user = User(row[0], row[1], row[2])  # this can be cls
        else:
            user = None

        connection.close()

        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        select_query = "SELECT * FROM user WHERE id=?"
        result = cursor.execute(select_query, (_id,))
        row = result.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()

        return user


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

        if User.find_by_username(request_data['username']):
            return {'message': 'Username already exists'}, 400

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        regitser_query = "INSERT INTO user VALUES (NULL, ?, ?)"
        cursor.execute(regitser_query, (request_data["username"], request_data["password"],))

        connection.commit()
        connection.close()

        return {"message": "User registered successfully."}, 201
