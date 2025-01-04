from flask import Blueprint, render_template, redirect, url_for
from backend.plex_invite.routes.shared import get_config

panel_bp = Blueprint('panel', __name__)

@panel_bp.route('/admin')
def admin_panel():
    config = get_config()
    if not config.is_initial_setup_complete():
        return redirect(url_for('setup.setup'))
    return render_template('admin.html')