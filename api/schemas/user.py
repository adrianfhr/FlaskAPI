from extensions import marshmallow
from models.user import User

from marshmallow import ValidationError, validate, validates_schema
from marshmallow.fields import String, Integer, UUID

class UserSchema(marshmallow.SQLAlchemyAutoSchema):
    
    email = String(required=True, validate=validate.Email())

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
        exclude = ['_password']

class UserCreateSchema(UserSchema):
    password = String(
        required=True,
        validate=[
            validate.Length(min=8),
            validate.Regexp(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$',
                error='Password must contain at least 8 characters long and include one uppercase letter, one lowercase letter, and one number'
            )
        ]
    )  # Menambahkan field password
    class Meta:
        model = User
        load_instance = True
        exclude = ['_password']