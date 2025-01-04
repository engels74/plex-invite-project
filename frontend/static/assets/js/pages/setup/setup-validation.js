import { showMessage } from './setup-messages.js';
import { createAdmin, testPlex, testSmtp, verifyAdmin } from './setup-api.js';

// Setup state management
const setupState = {
    admin: {
        validated: false,
        saved: false
    },
    plex: {
        validated: false,
        saved: false
    },
    smtp: {
        validated: false,
        saved: false
    }
};

// Update navigation button state
function updateNavigation() {
    const currentStep = document.querySelector('.setup-step.active').id;
    const nextButton = document.getElementById('next-step');
    
    switch (currentStep) {
        case 'step-admin':
            nextButton.disabled = !setupState.admin.saved;
            break;
        case 'step-plex':
            nextButton.disabled = !setupState.plex.saved;
            break;
        case 'step-smtp':
            nextButton.disabled = !setupState.smtp.saved;
            break;
    }
}

export function initializeFormValidations() {
    // Admin form
    document.getElementById('admin-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        const submitBtn = this.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        const formData = {
            username: document.getElementById('admin_username').value,
            password: document.getElementById('admin_password').value,
            confirm_password: document.getElementById('confirm_password').value
        };
        
        try {
            const success = await createAdmin(formData);
            if (success) {
                setupState.admin.saved = true;
                updateNavigation();
                
                // Disable form fields
                const form = document.getElementById('admin-form');
                form.querySelectorAll('input').forEach(input => {
                    input.disabled = true;
                    input.classList.add('opacity-50', 'cursor-not-allowed');
                });

                // Update submit button
                const submitBtn = form.querySelector('button[type="submit"]');
                submitBtn.disabled = true;
                submitBtn.textContent = 'Account Created';
                submitBtn.classList.remove('bg-plex-orange', 'hover:bg-plex-orange/90');
                submitBtn.classList.add('bg-green-600', 'cursor-not-allowed');

                // Update step header
                const stepHeader = document.querySelector('#step-admin h3');
                stepHeader.innerHTML = `
                    <span class="text-green-500">✓</span>
                    Step 1: Admin Account <span class="text-sm text-green-500">(Completed)</span>
                `;

                // Enable next step button
                document.getElementById('next-step').disabled = false;
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage('An error occurred while creating admin account', 'error');
        }
    });

    // Plex form
    document.getElementById('plex-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        if (this.dataset.disabled === 'true' || this.dataset.processing === 'true') return;
        this.dataset.processing = 'true';
        try {
            const success = await testPlex(true); // Quiet mode
            if (success) {
                setupState.plex.saved = true;
                updateNavigation();
                
                // Disable form fields
                const form = document.getElementById('plex-form');
                form.querySelectorAll('input').forEach(input => {
                    input.disabled = true;
                    input.classList.add('opacity-50', 'cursor-not-allowed');
                });

                // Update save button and disable form submission
                const saveBtn = form.querySelector('button[type="submit"]');
                saveBtn.disabled = true;
                saveBtn.textContent = 'Settings Saved';
                saveBtn.classList.remove('bg-plex-orange', 'hover:bg-plex-orange/90');
                saveBtn.classList.add('bg-green-600', 'cursor-not-allowed');
                form.dataset.disabled = 'true';

                // Update step header
                const stepHeader = document.querySelector('#step-plex h3');
                stepHeader.innerHTML = `
                    <span class="text-green-500">✓</span>
                    Step 2: Plex Configuration <span class="text-sm text-green-500">(Completed)</span>
                `;

                // Remove existing Clear button if present
                const existingClearBtn = form.querySelector('.clear-btn');
                if (existingClearBtn) {
                    existingClearBtn.remove();
                }

                // Add Clear button
                const clearBtn = document.createElement('button');
                clearBtn.type = 'button';
                clearBtn.className = 'clear-btn flex-1 px-4 py-2 border border-plex-orange/30 text-plex-orange rounded-lg hover:bg-plex-orange/10 transition-colors';
                clearBtn.textContent = 'Clear';
                clearBtn.addEventListener('click', async () => {
                    // Show confirmation dialog
                    const confirmed = confirm('Are you sure you want to clear Plex settings? This will remove the configuration from the database.');
                    if (!confirmed) return;

                    try {
                        // Call API to clear settings
                        const response = await fetch('/api/setup/clear-plex', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            }
                        });
                        
                        const data = await response.json();
                        if (response.ok) {
                            // Enable form fields
                            form.querySelectorAll('input').forEach(input => {
                                input.disabled = false;
                                input.classList.remove('opacity-50', 'cursor-not-allowed');
                            });

                            // Reset save button and enable form submission
                            saveBtn.disabled = false;
                            saveBtn.textContent = 'Save Plex Settings';
                            saveBtn.classList.remove('bg-green-600', 'cursor-not-allowed');
                            saveBtn.classList.add('bg-plex-orange', 'hover:bg-plex-orange/90');
                            form.dataset.disabled = 'false';

                            // Reset step header
                            stepHeader.innerHTML = 'Step 2: Configure Plex Server';

                            // Remove Clear button
                            clearBtn.remove();

                            // Update state
                            setupState.plex.saved = false;
                            updateNavigation();
                            
                            showMessage(data.message, 'success');
                        } else {
                            throw new Error(data.error || 'Failed to clear Plex settings');
                        }
                    } catch (error) {
                        console.error('Error:', error);
                        showMessage(error.message, 'error');
                    }
                });

                // Insert Clear button next to Save button
                const buttonContainer = form.querySelector('.flex.gap-4');
                buttonContainer.appendChild(clearBtn);
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage('An error occurred while saving Plex settings', 'error');
        } finally {
            this.dataset.processing = 'false';
        }
    });

    // SMTP form
    document.getElementById('smtp-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        if (this.dataset.disabled === 'true' || this.dataset.processing === 'true') return;
        this.dataset.processing = 'true';
        try {
            const success = await testSmtp(true); // Quiet mode
            if (success) {
                setupState.smtp.saved = true;
                updateNavigation();
                
                // Disable form fields
                const form = document.getElementById('smtp-form');
                form.querySelectorAll('input').forEach(input => {
                    input.disabled = true;
                    input.classList.add('opacity-50', 'cursor-not-allowed');
                });

                // Update save button and disable form submission
                const saveBtn = form.querySelector('button[type="submit"]');
                saveBtn.disabled = true;
                saveBtn.textContent = 'Settings Saved';
                saveBtn.classList.remove('bg-plex-orange', 'hover:bg-plex-orange/90');
                saveBtn.classList.add('bg-green-600', 'cursor-not-allowed');
                form.dataset.disabled = 'true';

                // Update step header
                const stepHeader = document.querySelector('#step-smtp h3');
                stepHeader.innerHTML = `
                    <span class="text-green-500">✓</span>
                    Step 3: SMTP Configuration <span class="text-sm text-green-500">(Completed)</span>
                `;

                // Remove existing Clear button if present
                const existingClearBtn = form.querySelector('.clear-btn');
                if (existingClearBtn) {
                    existingClearBtn.remove();
                }

                // Add Clear button
                const clearBtn = document.createElement('button');
                clearBtn.type = 'button';
                clearBtn.className = 'clear-btn flex-1 px-4 py-2 border border-plex-orange/30 text-plex-orange rounded-lg hover:bg-plex-orange/10 transition-colors';
                clearBtn.textContent = 'Clear';
                clearBtn.addEventListener('click', async () => {
                    // Show confirmation dialog
                    const confirmed = confirm('Are you sure you want to clear SMTP settings? This will remove the configuration from the database.');
                    if (!confirmed) return;

                    try {
                        // Call API to clear settings
                        const response = await fetch('/api/setup/clear-smtp', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            }
                        });
                        
                        const data = await response.json();
                        if (response.ok) {
                            // Enable form fields
                            form.querySelectorAll('input').forEach(input => {
                                input.disabled = false;
                                input.classList.remove('opacity-50', 'cursor-not-allowed');
                            });

                            // Reset save button and enable form submission
                            saveBtn.disabled = false;
                            saveBtn.textContent = 'Save SMTP Settings';
                            saveBtn.classList.remove('bg-green-600', 'cursor-not-allowed');
                            saveBtn.classList.add('bg-plex-orange', 'hover:bg-plex-orange/90');
                            form.dataset.disabled = 'false';

                            // Reset step header
                            stepHeader.innerHTML = 'Step 3: Configure SMTP';

                            // Remove Clear button
                            clearBtn.remove();

                            // Update state
                            setupState.smtp.saved = false;
                            updateNavigation();
                            
                            showMessage(data.message, 'success');
                        } else {
                            throw new Error(data.error || 'Failed to clear SMTP settings');
                        }
                    } catch (error) {
                        console.error('Error:', error);
                        showMessage(error.message, 'error');
                    }
                });

                // Insert Clear button next to Save button
                const buttonContainer = form.querySelector('.flex.gap-4');
                buttonContainer.appendChild(clearBtn);
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage('An error occurred while saving SMTP settings', 'error');
        } finally {
            this.dataset.processing = 'false';
        }
    });

    // Test Plex connection button
    document.getElementById('test-plex').addEventListener('click', async function() {
        const testBtn = this;
        testBtn.disabled = true;
        testBtn.textContent = 'Testing...';

        try {
            const success = await testPlex();
            if (success) {
                setupState.plex.validated = true;
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage('Error testing Plex connection', 'error');
        } finally {
            testBtn.disabled = false;
            testBtn.textContent = 'Test Connection';
        }
    });

    // Test SMTP connection button
    document.getElementById('test-smtp').addEventListener('click', async function() {
        const testBtn = this;
        testBtn.disabled = true;
        testBtn.textContent = 'Testing...';

        try {
            const success = await testSmtp();
            if (success) {
                setupState.smtp.validated = true;
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage('Error testing SMTP connection', 'error');
        } finally {
            testBtn.disabled = false;
            testBtn.textContent = 'Test SMTP';
        }
    });

    // Initialize navigation state
    updateNavigation();
}