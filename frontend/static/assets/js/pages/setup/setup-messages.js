export function showMessage(message, type = 'info') {
    const container = document.getElementById('message-container');
    const messageDiv = document.createElement('div');
    
    // Set base classes and icon based on message type
    let iconPath = '';
    switch(type) {
        case 'success':
            messageDiv.className = 'success-message';
            iconPath = '<path stroke-linecap="round" stroke-linejoin="round" d="M4 12l5 5 8-8" />';
            break;
        case 'error':
            messageDiv.className = 'error-message';
            iconPath = '<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>';
            break;
        default:
            messageDiv.className = 'info-message';
            iconPath = '<path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>';
    }

    // Create icon SVG
    const icon = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    icon.setAttribute('class', `${type}-icon`);
    icon.setAttribute('viewBox', '0 0 20 20');
    icon.setAttribute('fill', 'none');
    icon.setAttribute('stroke', 'currentColor');
    icon.setAttribute('stroke-width', '2');
    icon.setAttribute('aria-hidden', 'true');
    icon.innerHTML = iconPath;

    // Create message text
    const text = document.createElement('span');
    text.textContent = message;

    // Append elements
    messageDiv.appendChild(icon);
    messageDiv.appendChild(text);
    container.appendChild(messageDiv);

    // Auto-remove message after 5 seconds
    setTimeout(() => {
        messageDiv.classList.add('fade-out');
        setTimeout(() => {
            messageDiv.remove();
        }, 300);
    }, 5000);
}