import uuid

from extensions import db
from sqlalchemy.dialects.postgresql import UUID
class TokenBlocklist(db.Model):
    __tablename__ = 'token_blocklist'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Use UUID as primary key
    jti = db.Column(db.String(120), nullable=False, unique=True)
    token_type = db.Column(db.String(120), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False, index=True)
    revoked_at = db.Column(db.DateTime)
    expires = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User')
    def __repr__(self):
        return f'<TokenBlocklist {self.jti}>'