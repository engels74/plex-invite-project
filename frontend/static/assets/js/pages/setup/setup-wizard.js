import { showMessage } from './setup-messages.js';
import { createAdmin, verifyAdmin, savePlex, saveSmtp, testPlex, testSmtp, completeSetup } from './setup-api.js';

export function initializeWizard() {
    const steps = document.querySelectorAll('.setup-step');
    let currentStep = 0;

    // Setup state tracking
    const setupState = {
        admin: false,
        plex: false,
        smtp: false
    };

    // Setup form submit handlers
    document.getElementById('plex-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        const submitButton = this.querySelector('button[type="submit"]');
        const testButton = document.getElementById('test-plex');
        
        // Check if form is already saved successfully
        if (submitButton.classList.contains('success')) return;
        
        // Disable both buttons during submission
        submitButton.disabled = true;
        testButton.disabled = true;
        
        try {
            const success = await savePlex();
            if (success) {
                const testSuccess = await testPlex(true); // Test connection after saving
                if (testSuccess) {
                    // On success, keep buttons disabled and update UI
                    submitButton.classList.add('success');
                    setupState.plex = true;
                    
                    // Disable all form inputs
                    this.querySelectorAll('input').forEach(input => {
                        input.disabled = true;
                        input.classList.add('opacity-50', 'cursor-not-allowed');
                    });
                    
                    // Update step header
                    const stepHeader = document.querySelector('#step-plex h3');
                    stepHeader.innerHTML = `
                        <span class="text-green-500">✓</span>
                        Step 2: Configure Plex Server <span class="text-sm text-green-500">(Completed)</span>
                    `;
                    
                    // Enable next step button
                    document.getElementById('next-step').disabled = false;
                } else {
                    // Re-enable buttons if test fails
                    submitButton.disabled = false;
                    testButton.disabled = false;
                }
            } else {
                // Re-enable buttons if save fails
                submitButton.disabled = false;
                testButton.disabled = false;
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage('Error saving Plex settings', 'error');
            submitButton.disabled = false;
            testButton.disabled = false;
        }
    });

    document.getElementById('smtp-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        const submitButton = this.querySelector('button[type="submit"]');
        const testButton = this.querySelector('button[type="button"]'); // Fixed selector
        
        // Check if form is already saved successfully
        if (submitButton.classList.contains('success')) return;
        
        // Disable both buttons during submission
        submitButton.disabled = true;
        if (testButton) testButton.disabled = true;
        
        try {
            const success = await saveSmtp();
            if (success) {
                const testSuccess = await testSmtp(true); // Test connection after saving
                if (testSuccess) {
                    // On success, keep buttons disabled and update UI
                    submitButton.classList.add('success');
                    setupState.smtp = true;
                    
                    // Disable all form inputs
                    this.querySelectorAll('input').forEach(input => {
                        input.disabled = true;
                        input.classList.add('opacity-50', 'cursor-not-allowed');
                    });
                    
                    // Update step header
                    const stepHeader = document.querySelector('#step-smtp h3');
                    stepHeader.innerHTML = `
                        <span class="text-green-500">✓</span>
                        Step 3: Configure SMTP <span class="text-sm text-green-500">(Completed)</span>
                    `;
                    
                    // Enable next step button
                    document.getElementById('next-step').disabled = false;
                } else {
                    // Re-enable buttons if test fails
                    submitButton.disabled = false;
                    if (testButton) testButton.disabled = false;
                }
            } else {
                // Re-enable buttons if save fails
                submitButton.disabled = false;
                if (testButton) testButton.disabled = false;
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage('Error saving SMTP settings', 'error');
            submitButton.disabled = false;
            if (testButton) testButton.disabled = false;
        }
    });

    // Add test button handlers
    document.getElementById('test-plex').addEventListener('click', async function() {
        const form = document.getElementById('plex-form');
        const submitButton = form.querySelector('button[type="submit"]');
        
        // Don't test if form is already saved successfully
        if (submitButton.classList.contains('success')) return;
        
        // Disable both buttons during test
        this.disabled = true;
        submitButton.disabled = true;
        
        try {
            await testPlex();
        } finally {
            // Re-enable buttons after test (unless form was saved successfully)
            if (!submitButton.classList.contains('success')) {
                this.disabled = false;
                submitButton.disabled = false;
            }
        }
    });

    document.getElementById('next-step').addEventListener('click', async function() {
        const nextBtn = this;
        nextBtn.disabled = true;

        try {
            let canProceed = false;
            
            if (currentStep === 0) {
                // Verify admin account exists
                canProceed = await verifyAdmin();
                if (canProceed) setupState.admin = true;
            } else if (currentStep === 1) {
                // Verify Plex settings
                canProceed = setupState.plex;
            } else if (currentStep === 2) {
                // On final step, verify all required settings
                canProceed = setupState.smtp;
                if (canProceed) {
                    // Verify all required settings are complete
                    if (!setupState.admin || !setupState.plex || !setupState.smtp) {
                        showMessage('Please complete all previous steps before finishing setup', 'error');
                        return;
                    }
                    
                    // Complete setup
                    const completeSuccess = await completeSetup();
                    if (completeSuccess) {
                        // Redirect will be handled by completeSetup
                        return;
                    }
                }
            }

            if (canProceed && currentStep < steps.length - 1) {
                steps[currentStep].classList.remove('active');
                currentStep++;
                steps[currentStep].classList.add('active');
                updateNavigation();
            }
        } catch (error) {
            console.error('Error:', error);
            showMessage('An error occurred while proceeding to next step', 'error');
        } finally {
            nextBtn.disabled = false;
        }
    });

    document.getElementById('prev-step').addEventListener('click', function() {
        if (currentStep > 0) {
            steps[currentStep].classList.remove('active');
            currentStep--;
            steps[currentStep].classList.add('active');
            updateNavigation();
        }
    });

    function updateNavigation() {
        document.getElementById('prev-step').disabled = currentStep === 0;
        document.getElementById('next-step').disabled = currentStep === steps.length - 1;
    }

    // Initialize step validation
    document.getElementById('next-step').disabled = true;
}