export async function makeApiCall(url, method = 'GET', body = null) {
    const headers = {
        'Content-Type': 'application/json',
    };

    const config = {
        method,
        headers,
        body: body ? JSON.stringify(body) : null
    };

    try {
        const response = await fetch(url, config);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

export function handleApiError(error, defaultMessage = 'An error occurred') {
    console.error('API Error:', error);
    return {
        error: error.message || defaultMessage
    };
}