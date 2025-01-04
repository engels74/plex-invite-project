from flask import Flask
from datetime import timedelta
from backend.plex_invite.routes.main.routes import main_bp
from backend.plex_invite.routes.setup.routes import setup_bp
from backend.plex_invite.routes.shared import get_config
from backend.plex_invite.routes.admin.panel.routes import panel_bp
from backend.plex_invite.routes.admin.users.routes import users_bp
from backend.plex_invite.routes.admin.auth import auth_bp
from backend.plex_invite.routes.keys.routes import keys_bp
from backend.plex_invite.routes.admin.smtp.routes import smtp_bp
from backend.plex_invite.routes.admin.onboarding.routes import onboarding_bp
from backend.plex_invite.core.plex.connection import PlexConnection

app = Flask(__name__,
            template_folder='frontend/templates',
            static_folder='frontend/static')
app.config['JWT_SECRET_KEY'] = 'your-secret-key-here'  # Should be from environment variable
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_ALGORITHM'] = 'HS256'
app.register_blueprint(main_bp)
app.register_blueprint(setup_bp)
app.register_blueprint(panel_bp)
app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(keys_bp)
app.register_blueprint(smtp_bp)
app.register_blueprint(onboarding_bp)

def get_plex_connection():
    """Get Plex connection if configured"""
    config = get_config()
    if config.plex is None:
        return None
    return PlexConnection(config.plex)

if __name__ == '__main__':
    from database.init_db import initialize_database
    initialize_database()
    app.run(debug=True)