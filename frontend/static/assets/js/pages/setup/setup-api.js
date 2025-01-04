import { showMessage } from './setup-messages.js';

export async function createAdmin(formData) {
    try {
        const response = await fetch('/api/setup/admin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage(data.message, 'success');
            return true;
        }
        
        showMessage(data.error || 'Error creating admin account', 'error');
        return false;
    } catch (error) {
        console.error('Error:', error);
        showMessage('An error occurred while creating admin account', 'error');
        return false;
    }
}

export async function verifyAdmin(retries = 3, delay = 500) {
    try {
        // Add delay to allow backend state to update
        await new Promise(resolve => setTimeout(resolve, delay));
        
        const response = await fetch('/api/setup/verify-admin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        console.log('verifyAdmin response:', { status: response.status, data });

        // Handle all valid states:
        // 1. Admin exists (200 status)
        // 2. No admin exists (400 status with specific message)
        if (response.ok || 
            (response.status === 400 && data.error === 'Admin account not found')) {
            return true;
        }
        
        // Handle retries for state synchronization issues
        if (retries > 0 && response.status === 400) {
            console.log(`Retrying verification... attempts left: ${retries}`);
            return await verifyAdmin(retries - 1, delay);
        }
        
        // Handle all other errors
        showMessage(data.error || 'Error verifying admin account', 'error');
        return false;
    } catch (error) {
        console.error('Error:', error);
        showMessage('Error verifying admin account', 'error');
        return false;
    }
}

export async function testPlex(quiet = false) {
    const formData = {
        url: document.getElementById('plex_url').value,
        token: document.getElementById('plex_token').value,
        quiet: quiet
    };

    try {
        const response = await fetch('/api/setup/test-plex', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        const data = await response.json();
        
        if (data.error) {
            showMessage(quiet ? 'Plex connection verification failed' : data.error, 'error');
            return false;
        }
        if (!quiet) showMessage(data.message, 'success');
        return true;
    } catch (error) {
        console.error('Error:', error);
        showMessage('Error verifying Plex connection', 'error');
        return false;
    }
}

export async function savePlex() {
    const formData = {
        url: document.getElementById('plex_url').value,
        token: document.getElementById('plex_token').value
    };

    try {
        const response = await fetch('/api/setup/save-plex', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        const data = await response.json();
        
        if (data.error) {
            showMessage(data.error, 'error');
            return false;
        }
        showMessage(data.message, 'success');
        return true;
    } catch (error) {
        console.error('Error:', error);
        showMessage('Error saving Plex settings', 'error');
        return false;
    }
}

export async function testSmtp(quiet = false) {
    const formData = {
        host: document.getElementById('smtp_host').value,
        port: parseInt(document.getElementById('smtp_port').value),
        username: document.getElementById('smtp_username').value,
        password: document.getElementById('smtp_password').value,
        from_email: document.getElementById('from_email').value,
        use_tls: document.getElementById('use_tls').checked,
        quiet: quiet
    };

    try {
        const response = await fetch('/api/setup/test-smtp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        const data = await response.json();
        
        if (data.error) {
            showMessage(quiet ? 'SMTP connection verification failed' : data.error, 'error');
            return false;
        }
        if (!quiet) showMessage(data.message, 'success');
        return true;
    } catch (error) {
        console.error('Error:', error);
        showMessage('Error verifying SMTP connection', 'error');
        return false;
    }
}

export async function saveSmtp() {
    const formData = {
        host: document.getElementById('smtp_host').value,
        port: parseInt(document.getElementById('smtp_port').value),
        username: document.getElementById('smtp_username').value,
        password: document.getElementById('smtp_password').value,
        from_email: document.getElementById('from_email').value,
        use_tls: document.getElementById('use_tls').checked
    };

    try {
        const response = await fetch('/api/setup/save-smtp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        const data = await response.json();
        
        if (data.error) {
            showMessage(data.error, 'error');
            return false;
        }
        showMessage(data.message, 'success');
        return true;
    } catch (error) {
        console.error('Error:', error);
        showMessage('Error saving SMTP settings', 'error');
        return false;
    }
}

export async function completeSetup() {
    try {
        const response = await fetch('/api/setup/complete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Handle redirect if provided
            if (data.redirect) {
                window.location.href = data.redirect;
                return true;
            }
            return true;
        }
        
        showMessage(data.error || 'Error completing setup', 'error');
        return false;
    } catch (error) {
        console.error('Error:', error);
        showMessage('Error completing setup', 'error');
        return false;
    }
}