
from flask_restful import Resource
from flask import request

from api.schemas.user import UserSchema
from models.user import User
from extensions import db


class UserList(Resource):
    def get(self):
        try:
            schema = UserSchema(many=True)
            users = User.query.all()
            return schema.dump(users)
        except Exception as e:
            return {"message": str(e)}, 400
    
    def post(self):
        try:
            schema = UserSchema()
            user = schema.load(request.get_json(), instance=User(), session=db.session)
            db.session.add(user)
            db.session.commit()

            return {"message": "User created successfully", "user": schema.dump(user)}, 201
        except Exception as e:
            return {"message": str(e)}, 400

class UserDetail(Resource):
    def get(self, user_id):
        try:
            schema = UserSchema()
            user = User.query.get(user_id)
            if user:
                return {"user" : schema.dump(user)}, 200
            return {"message": "User not found"}, 404
        except Exception as e:
            return {"message": str(e)}, 400

    def put(self, user_id):
       
            schema = UserSchema(partial=True)
            user = User.query.get(user_id)
            if user:
                user = schema.load(request.get_json(), instance=user)
                db.session.add(user)
                db.session.commit()
                return {"message": "User updated successfully", "user": schema.dump(user)}, 200
            return {"message": "User not found"}, 404
        

    def delete(self, user_id):
        try:
            user = User.query.get(user_id)
            if user:
                db.session.delete(user)
                db.session.commit()
                return {"message": "User deleted successfully"}, 200
            return {"message": "User not found"}, 404
        except Exception as e:
            return {"message": str(e)}, 400


    