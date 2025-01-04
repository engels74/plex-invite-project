from flask import Blueprint, render_template, redirect, url_for
from backend.plex_invite.routes.shared import get_config

onboarding_bp = Blueprint('onboarding', __name__)

@onboarding_bp.route('/admin/onboarding')
def admin_onboarding():
    config = get_config()
    if not config.is_initial_setup_complete():
        return redirect(url_for('setup.setup'))
    return render_template('admin_onboarding.html')