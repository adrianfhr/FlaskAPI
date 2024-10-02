
from flask_restful import Resource
from flask import  jsonify, request

from models.user import User
from extensions import db


class UserList(Resource):
    def get(self):
        users = User.query.all()
        return jsonify(users)
    
    def post(self):

        data = request.get_json()

        user = User(
            username=data.get('username'),
            email=data.get('email'),
            age=data.get('age'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        ) 

        db.session.add(user)
        db.session.commit()

        return jsonify(msg="User created", user=user)

class UserDetail(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return jsonify(user)
    
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        data = request.get_json()

        user.username = data['username']
        user.email = data['email']
        user.age = data['age']
        user.first_name = data['first_name']
        user.last_name = data['last_name']

        db.session.commit()

        return jsonify(user)
    
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)

        db.session.delete(user)
        db.session.commit()

        return '', 204


    