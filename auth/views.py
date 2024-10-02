from flask import Blueprint, request
from marshmallow import ValidationError

from api.schemas.user import UserSchema, UserCreateSchema
from auth.helpers import add_token_to_database, is_token_revoked, revoke_token
from extensions import db, pwd_context, jwt
from models.user import User
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt, get_jwt_identity, jwt_required
from flask import current_app as app 
auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")

@auth_blueprint.route("/register", methods=["POST"])
def register():
    try:
        schema = UserCreateSchema()
        user = schema.load(request.get_json())
        db.session.add(user)
        db.session.commit()

        schema = UserSchema()

        return {"message": "User created successfully", "user": schema.dump(user)}, 201
    except Exception as e:
        return {"message": str(e)}, 400

@auth_blueprint.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        user = User.query.filter(User.username == username).first()

        if not user or not pwd_context.verify(password, user.password):
            return {"message": "Invalid username or password"}, 400

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        add_token_to_database(access_token)
        add_token_to_database(refresh_token)

        return {"access_token": access_token, "refresh_token": refresh_token}, 200
    except Exception as e:
        return {"message": str(e)}, 400

@auth_blueprint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id)
        add_token_to_database(access_token)
        return {"access_token": access_token}, 200
    except Exception as e:
        return {"message": str(e)}, 400

@auth_blueprint.route("/revoke_access", methods=["DELETE"])
@jwt_required()
def revoke_access():
    try:
        user_id = get_jwt_identity()
        jti = get_jwt()["jti"]
        revoke_token(jti, user_id)
        return {"message": "Access token has been revoked"}, 200
    except Exception as e:
        return {"message": str(e)}, 400
    
@auth_blueprint.route("/revoke_refresh", methods=["DELETE"])
@jwt_required(refresh=True)
def revoke_access_token():
    try:
        user_id = get_jwt_identity()
        jti = get_jwt()["jti"]
        revoke_token(jti, user_id)
        return {"message": "Refresh token has been revoked"}, 200
    except Exception as e:
        return {"message": str(e)}, 400

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_headers, jwt_payload):
    return is_token_revoked(jwt_payload)

@jwt.user_lookup_loader
def load_user(jwt_headers, jwt_payload):
    user_id = jwt_payload[app.config.get('JWT_IDENTITY_CLAIM')]
    return User.query.get(user_id)

@auth_blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(error):
    return {"message": "Validation error", "errors": error.messages}, 400