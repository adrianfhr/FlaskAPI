import uuid
from sqlalchemy.dialects.postgresql import UUID
from extensions import db
from dataclasses import dataclass, field

@dataclass
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Use UUID as primary key
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'
