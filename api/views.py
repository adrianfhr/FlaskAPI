from flask import Blueprint, jsonify 
from flask_restful import Api
from api.resources.user import UserList, UserDetail
from marshmallow import ValidationError

blueprint = Blueprint("api", __name__, url_prefix="/api")

api = Api(blueprint, errors=blueprint.errorhandler)

api.add_resource(UserList, "/users")
api.add_resource(UserDetail, "/users/<uuid:user_id>")


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(error):
    return {"message": "Validation error", "errors": error.messages}, 400