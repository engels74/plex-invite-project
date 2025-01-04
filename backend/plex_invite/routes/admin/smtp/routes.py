from flask import Blueprint, render_template, redirect, url_for
from backend.plex_invite.routes.shared import get_config

smtp_bp = Blueprint('smtp', __name__)

@smtp_bp.route('/admin/smtp')
def admin_smtp():
    config = get_config()
    if not config.is_initial_setup_complete():
        return redirect(url_for('setup.setup'))
    return render_template('admin_smtp.html', config=config.smtp)