from datetime import datetime
from flask_jwt_extended import decode_token
from flask import current_app as app
from extensions import db
from models.auth import TokenBlocklist
from sqlalchemy.exc import NoResultFound
def add_token_to_database(encoded_token):
    decoded_token = decode_token(encoded_token)
    jti = decoded_token['jti']
    token_type = decoded_token['type']
    user_identity = decoded_token[app.config.get('JWT_IDENTITY_CLAIM')]
    expires = datetime.fromtimestamp(decoded_token['exp'])

    db_token = TokenBlocklist(
        jti=jti,
        token_type=token_type,
        user_id=user_identity,
        expires=expires,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.session.add(db_token)
    db.session.commit()

def revoke_token(jti, user_id):
    try:
        token = TokenBlocklist.query.filter_by(jti=jti, user_id=user_id).one()
        token.revoked_at = datetime.now()
        db.session.commit()
    except NoResultFound:
        raise Exception("Token is not in the database")
    
def is_token_revoked(jwt_payload):
    jti = jwt_payload['jti']
    user_id = jwt_payload[app.config.get('JWT_IDENTITY_CLAIM')]
    try:
        token = TokenBlocklist.query.filter_by(jti=jti, user_id=user_id).one()
        return bool(token.revoked_at is not None)
    except NoResultFound:
        raise Exception("Token is not in the database")