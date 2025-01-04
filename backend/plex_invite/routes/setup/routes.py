from flask import Blueprint, request, jsonify, render_template
from backend.plex_invite.core.database import SessionLocal
from backend.plex_invite.core.database.models import AdminUser, SetupState
from backend.plex_invite.core.plex.connection import PlexConnection
from backend.plex_invite.core.plex.config import PlexConnectionConfig
from backend.plex_invite.core.smtp.sender import SMTPSender
from backend.plex_invite.core.smtp.config import SMTPConfig
import bcrypt
import re
from datetime import datetime

setup_bp = Blueprint('setup', __name__)

def get_setup_state(db):
    state = db.query(SetupState).first()
    if not state:
        state = SetupState()
        db.add(state)
        db.commit()
    return state

@setup_bp.route('/setup', methods=['GET'])
def setup():
    """Render the setup page"""
    db = SessionLocal()
    get_setup_state(db)  # Ensure setup state exists
    db.close()
    return render_template('setup.html')

def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number"
    return True, ""

@setup_bp.route('/api/setup/admin', methods=['POST'])
def create_admin():
    db = SessionLocal()
    state = get_setup_state(db)
    
    # Check if admin user already exists
    if db.query(AdminUser).first():
        db.close()
        return jsonify({"error": "Admin account already exists"}), 400

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if not username or not password or not confirm_password:
        db.close()
        return jsonify({"error": "All fields are required"}), 400

    if password != confirm_password:
        db.close()
        return jsonify({"error": "Passwords do not match"}), 400

    is_valid, message = validate_password(password)
    if not is_valid:
        db.close()
        return jsonify({"error": message}), 400

    if db.query(AdminUser).filter(AdminUser.username == username).first():
        db.close()
        return jsonify({"error": "Username already exists"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    admin_user = AdminUser(
        username=username,
        password_hash=hashed_password.decode('utf-8')
    )
    
    db.add(admin_user)
    db.query(SetupState).filter(SetupState.id == state.id).update({
        "admin_created": True
    })
    db.commit()
    db.close()

    return jsonify({"message": "Admin account created successfully"})

@setup_bp.route('/api/setup/test-plex', methods=['POST'])
def test_plex_connection():
    db = SessionLocal()
    state = get_setup_state(db)
    
    data = request.get_json()
    url = data.get('url')
    token = data.get('token')
    quiet = data.get('quiet', False)

    if not url or not token:
        db.close()
        return jsonify({"error": "Plex URL and token are required"}), 400

    try:
        config = PlexConnectionConfig(base_url=url, token=token)
        plex = PlexConnection(config)
        if plex.test_connection():
            db.close()
            return jsonify({"message": "Plex connection successful"})
        db.close()
        if quiet:
            return jsonify({"error": ""}), 400
        return jsonify({"error": "Failed to connect to Plex server"}), 400
    except Exception as e:
        db.close()
        if quiet:
            return jsonify({"error": ""}), 400
        return jsonify({"error": str(e)}), 500

@setup_bp.route('/api/setup/save-plex', methods=['POST'])
def save_plex_settings():
    db = SessionLocal()
    state = get_setup_state(db)
    
    if not db.query(SetupState).filter(SetupState.id == state.id, SetupState.admin_created).first():
        db.close()
        return jsonify({"error": "Please complete admin setup first"}), 400

    data = request.get_json()
    url = data.get('url')
    token = data.get('token')

    if not url or not token:
        db.close()
        return jsonify({"error": "Plex URL and token are required"}), 400

    try:
        config = PlexConnectionConfig(base_url=url, token=token)
        plex = PlexConnection(config)
        if plex.test_connection():
            # Save Plex configuration
            from backend.plex_invite.config import ConfigLoader
            config_loader = ConfigLoader()
            app_config = config_loader.load()
            app_config.plex = config
            config_loader.save(app_config)
            
            # Update setup state
            db.query(SetupState).filter(SetupState.id == state.id).update({
                "plex_configured": True
            })
            db.commit()
            db.close()
            return jsonify({"message": "Plex settings saved successfully"})
        db.close()
        return jsonify({"error": "Failed to connect to Plex server"}), 400
    except Exception as e:
        db.close()
        return jsonify({"error": str(e)}), 500

@setup_bp.route('/api/setup/verify-admin', methods=['POST'])
def verify_admin():
    db = SessionLocal()
    get_setup_state(db)  # Ensure setup state exists
    
    admin_exists = db.query(AdminUser).first() is not None
    db.close()
    
    if not admin_exists:
        return jsonify({"error": "Admin account not found"}), 400
    return jsonify({"message": "Admin account verified"})

@setup_bp.route('/api/setup/test-smtp', methods=['POST'])
def test_smtp():
    db = SessionLocal()
    state = get_setup_state(db)
    
    data = request.get_json()
    host = data.get('host')
    port = data.get('port')
    username = data.get('username')
    password = data.get('password')
    from_email = data.get('from_email')
    use_tls = data.get('use_tls', False)
    quiet = data.get('quiet', False)

    if not all([host, port, username, password, from_email]):
        db.close()
        return jsonify({"error": "All SMTP fields are required"}), 400

    try:
        config = SMTPConfig(
            host=host,
            port=port,
            username=username,
            password=password,
            from_email=from_email,
            use_tls=use_tls,
            timeout=30
        )
        smtp = SMTPSender(config)
        if smtp.test_connection():
            db.close()
            return jsonify({"message": "SMTP connection successful"})
        db.close()
        if quiet:
            return jsonify({"error": ""}), 400
        return jsonify({"error": "Failed to connect to SMTP server"}), 400
    except Exception as e:
        db.close()
        if quiet:
            return jsonify({"error": ""}), 400
        return jsonify({"error": str(e)}), 500

@setup_bp.route('/api/setup/save-smtp', methods=['POST'])
def save_smtp_settings():
    db = SessionLocal()
    state = get_setup_state(db)
    
    if not db.query(SetupState).filter(SetupState.id == state.id, SetupState.admin_created).first():
        db.close()
        return jsonify({"error": "Please complete admin setup first"}), 400
    if not db.query(SetupState).filter(SetupState.id == state.id, SetupState.plex_configured).first():
        db.close()
        return jsonify({"error": "Please configure Plex first"}), 400

    data = request.get_json()
    host = data.get('host')
    port = data.get('port')
    username = data.get('username')
    password = data.get('password')
    from_email = data.get('from_email')
    use_tls = data.get('use_tls', False)

    if not all([host, port, username, password, from_email]):
        db.close()
        return jsonify({"error": "All SMTP fields are required"}), 400

    try:
        config = SMTPConfig(
            host=host,
            port=port,
            username=username,
            password=password,
            from_email=from_email,
            use_tls=use_tls,
            timeout=30
        )
        smtp = SMTPSender(config)
        if smtp.test_connection():
            # Save SMTP configuration
            from backend.plex_invite.config import ConfigLoader
            config_loader = ConfigLoader()
            app_config = config_loader.load()
            app_config.smtp = config
            config_loader.save(app_config)
            
            # Update setup state
            db.query(SetupState).filter(SetupState.id == state.id).update({
                "smtp_configured": True
            })
            db.commit()
            db.close()
            return jsonify({"message": "SMTP settings saved successfully"})
        db.close()
        return jsonify({"error": "Failed to connect to SMTP server"}), 400
    except Exception as e:
        db.close()
        return jsonify({"error": str(e)}), 500

@setup_bp.route('/api/setup/complete', methods=['POST'])
def complete_setup():
    """Finalize setup and redirect to admin panel"""
    db = SessionLocal()
    state = get_setup_state(db)
    
    # Verify all setup steps are complete
    if not all([
        state.admin_created,
        state.plex_configured,
        state.smtp_configured
    ]):
        db.close()
        return jsonify({"error": "Setup not complete"}), 400
    
    # Mark setup as complete
    db.query(SetupState).filter(SetupState.id == state.id).update({
        "setup_complete": True
    })
    db.commit()
    db.close()
    
    return jsonify({
        "message": "Setup completed successfully",
        "redirect": "/admin"
    })

@setup_bp.route('/api/setup/clear-plex', methods=['POST'])
def clear_plex_settings():
    db = SessionLocal()
    state = get_setup_state(db)
    
    try:
        # Clear Plex configuration
        from backend.plex_invite.config import ConfigLoader
        config_loader = ConfigLoader()
        app_config = config_loader.load()
        app_config.plex = None
        config_loader.save(app_config)
        
        # Update setup state
        db.query(SetupState).filter(SetupState.id == state.id).update({
            "plex_configured": False
        })
        db.commit()
        db.close()
        return jsonify({"message": "Plex settings cleared successfully"})
    except Exception as e:
        db.close()
        return jsonify({"error": str(e)}), 500

@setup_bp.route('/api/setup/clear-smtp', methods=['POST'])
def clear_smtp_settings():
    db = SessionLocal()
    state = get_setup_state(db)
    
    try:
        # Clear SMTP configuration
        from backend.plex_invite.config import ConfigLoader
        config_loader = ConfigLoader()
        app_config = config_loader.load()
        app_config.smtp = None
        config_loader.save(app_config)
        
        # Update setup state
        db.query(SetupState).filter(SetupState.id == state.id).update({
            "smtp_configured": False
        })
        db.commit()
        db.close()
        return jsonify({"message": "SMTP settings cleared successfully"})
    except Exception as e:
        db.close()
        return jsonify({"error": str(e)}), 500