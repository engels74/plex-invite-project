export function disableElement(element, text = 'Loading...') {
    if (element) {
        element.disabled = true;
        if (text && element.tagName === 'BUTTON') {
            element.textContent = text;
        }
    }
}

export function enableElement(element, originalText = '') {
    if (element) {
        element.disabled = false;
        if (originalText && element.tagName === 'BUTTON') {
            element.textContent = originalText;
        }
    }
}

export function createElement(tag, classes = [], attributes = {}) {
    const element = document.createElement(tag);
    if (classes.length > 0) {
        element.classList.add(...classes);
    }
    Object.entries(attributes).forEach(([key, value]) => {
        element.setAttribute(key, value);
    });
    return element;
}