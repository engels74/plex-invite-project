from datetime import datetime, timedelta
from functools import wraps
import jwt
from flask import request, jsonify, current_app
from backend.plex_invite.core.database import SessionLocal
from backend.plex_invite.core.database.models import AdminUser
from werkzeug.security import check_password_hash

def create_access_token(user_id):
    expires_delta = timedelta(minutes=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
    to_encode = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + expires_delta
    }
    encoded_jwt = jwt.encode(
        to_encode,
        current_app.config['JWT_SECRET_KEY'],
        algorithm=current_app.config['JWT_ALGORITHM']
    )
    return encoded_jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
            
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
            
        try:
            data = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=[current_app.config['JWT_ALGORITHM']]
            )
            current_user = SessionLocal().query(AdminUser).get(data['sub'])
        except Exception as e:
            return jsonify({"message": "Token is invalid!", "error": str(e)}), 401
            
        return f(current_user, *args, **kwargs)
    return decorated

def authenticate_user(username, password):
    db = SessionLocal()
    user = db.query(AdminUser).filter(AdminUser.username == username).first()
    if user and check_password_hash(user.password_hash.value, password):
        return user
    return None