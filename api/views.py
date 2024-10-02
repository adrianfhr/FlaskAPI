from flask import Blueprint, jsonify
from flask_restful import Api
from api.resources.user import UserList, UserDetail
from marshmallow import ValidationError
from flask_jwt_extended import JWTManager

# Inisialisasi blueprint
blueprint = Blueprint("api", __name__, url_prefix="/api")

# Inisialisasi API
api = Api(blueprint)

# Tambahkan resource
api.add_resource(UserList, "/users")
api.add_resource(UserDetail, "/users/<uuid:user_id>")

# Handler untuk marshmallow ValidationError
@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(error):
    return jsonify({"message": "Validation error", "errors": error.messages}), 400

# Handler untuk JWT error
@blueprint.errorhandler(401)  # Unauthorized
def handle_unauthorized(error):
    return jsonify({"message": "Authorization token is missing or invalid"}), 401

@blueprint.errorhandler(403)  # Forbidden
def handle_forbidden(error):
    return jsonify({"message": "You do not have permission to access this resource"}), 403

@blueprint.errorhandler(404)  # Not Found
def handle_not_found(error):
    return jsonify({"message": "Resource not found"}), 404

@blueprint.errorhandler(Exception)  # General exception handler
def handle_general_exception(error):
    return jsonify({"message": "An unexpected error occurred", "details": str(error)}), 500
