from flask import Blueprint, request, jsonify, current_app
from backend.plex_invite.core.auth import authenticate_user, create_access_token, token_required
from backend.plex_invite.core.database import SessionLocal
from backend.plex_invite.core.database.models import AdminUser
import bcrypt

auth_bp = Blueprint('auth', __name__)

def has_admin_users():
    db = SessionLocal()
    return db.query(AdminUser).count() > 0

@auth_bp.route('/admin/login', methods=['POST'])
def login():
    if not has_admin_users():
        return jsonify({
            "message": "No admin users found",
            "setup_required": True
        }), 403
        
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400
        
    user = authenticate_user(username, password)
    if not user:
        return jsonify({"message": "Invalid credentials"}), 401
        
    access_token = create_access_token(user.id)
    return jsonify({
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": current_app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds()
    })

@auth_bp.route('/admin/setup', methods=['POST'])
def setup_admin():
    if has_admin_users():
        return jsonify({"message": "Admin user already exists"}), 400
        
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400
        
    db = SessionLocal()
    if db.query(AdminUser).filter(AdminUser.username == username).first():
        return jsonify({"message": "Username already exists"}), 400
        
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    admin_user = AdminUser(
        username=username,
        password_hash=hashed_password.decode('utf-8')
    )
    
    db.add(admin_user)
    db.commit()
    
    return jsonify({
        "message": "Admin user created successfully",
        "username": username
    })

@auth_bp.route('/admin/logout', methods=['POST'])
@token_required
def logout(current_user):
    # In a real implementation, you'd add token to a blacklist
    return jsonify({"message": "Successfully logged out"})

@auth_bp.route('/admin/refresh', methods=['POST'])
@token_required
def refresh_token(current_user):
    new_token = create_access_token(current_user.id)
    return jsonify({
        "access_token": new_token,
        "token_type": "bearer",
        "expires_in": current_app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds()
    })