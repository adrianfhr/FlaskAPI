from extensions import marshmallow
from models.user import User

from marshmallow import ValidationError, validate, validates_schema
from marshmallow.fields import String, Integer, UUID

class UserSchema(marshmallow.SQLAlchemyAutoSchema):
    id = UUID(dump_only=True)  # Menambahkan ID sebagai field UUID dan dump_only
    username = String(required=True)
    email = String(required=True, validate=validate.Email())
    age = Integer(required=True)
    first_name = String(required=True)
    last_name = String(required=True)

    @validates_schema
    def validate_data(self, data, **kwargs):
        username = data.get('username')
        email = data.get('email')
        
        # Validasi untuk username and email yang unik
        if User.query.filter(User.username == username).first():
            raise ValidationError('Username already exists')
        if User.query.filter(User.email == email).first():
            raise ValidationError('Email already exists')

    class Meta:
        model = User
        load_instance = True