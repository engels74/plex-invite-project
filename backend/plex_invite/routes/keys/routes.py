from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from datetime import timedelta
from backend.plex_invite.routes.shared import get_config, get_plex_connection
from backend.plex_invite.core.access_keys.manager import AccessKeyManager
from backend.plex_invite.core.plex.library import PlexLibraryManager
from backend.plex_invite.core.access_keys.generator import AccessKeyConfig

keys_bp = Blueprint('keys', __name__)

@keys_bp.route('/admin/keys')
def admin_keys():
    config = get_config()
    if not config.is_initial_setup_complete():
        return redirect(url_for('setup.setup'))
        
    plex_connection = get_plex_connection()
    if plex_connection is None:
        return redirect(url_for('setup.setup'))
        
    # Initialize managers
    access_key_manager = AccessKeyManager()
    library_manager = PlexLibraryManager(plex_connection)
    
    # Get existing keys and libraries
    keys = [
        {
            'key': record.key,
            'created_at': record.created_at,
            'expires_at': record.created_at + timedelta(days=record.config.valid_days),
            'uses': record.uses,
            'max_uses': record.config.max_uses,
            'is_active': record.is_active
        }
        for record in access_key_manager._keys.values()
    ]
    libraries = library_manager.get_libraries()
    
    return render_template('admin_keys.html', keys=keys, libraries=libraries)

@keys_bp.route('/admin/keys/create', methods=['POST'])
def create_key():
    config = get_config()
    if not config.is_initial_setup_complete():
        return jsonify({'success': False, 'error': 'Setup not complete'}), 400
        
    data = request.get_json()
    
    try:
        config = AccessKeyConfig(
            valid_days=int(data['valid_days']),
            max_uses=int(data['max_uses']),
            libraries=data['libraries']
        )
        
        access_key_manager = AccessKeyManager()
        key_record = access_key_manager.create_key(config)
        
        return jsonify({
            'success': True,
            'key': key_record.key,
            'expires_at': (key_record.created_at + timedelta(days=config.valid_days)).isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400