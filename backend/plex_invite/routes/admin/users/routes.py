from flask import Blueprint, render_template, redirect, url_for
from backend.plex_invite.routes.shared import get_config
from backend.plex_invite.core.users.manager import UserManager
from backend.plex_invite.routes.shared import get_plex_connection

users_bp = Blueprint('users', __name__)

@users_bp.route('/admin/users')
def admin_users():
    config = get_config()
    if not config.is_initial_setup_complete():
        return redirect(url_for('setup.setup'))
        
    plex_connection = get_plex_connection()
    if plex_connection is None:
        return redirect(url_for('setup.setup'))
        
    user_manager = UserManager(plex_connection)
    users = user_manager.get_users()
    return render_template('admin_users.html', users=users)