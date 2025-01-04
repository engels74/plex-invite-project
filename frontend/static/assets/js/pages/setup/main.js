import { initializeWizard } from './setup-wizard.js';
import { initializeFormValidations } from './setup-validation.js';

document.addEventListener('DOMContentLoaded', () => {
    initializeWizard();
    initializeFormValidations();
});