import { API_URL } from '../constants.ts';

const getHeaders = () => {
    return {
        'Content-Type': 'application/json',
        Authorization: `Bearer }`,
    };
};

async function handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
        const error = await response.json().catch(() => ({ message: 'An unexpected error occurred' }));
        throw new Error(error.message || `Error: ${response.status}`);
    }
    return response.json();
}

export const apiClient = {
    get: <T>(endpoint: string) => fetch(`${API_URL}${endpoint}`).then((res) => handleResponse<T>(res)),

    post: <T>(endpoint: string, data: T) =>
        fetch(`${API_URL}${endpoint}`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(data),
        }).then((res) => handleResponse<T>(res)),

    put: <T>(endpoint: string, data: T) =>
        fetch(`${API_URL}${endpoint}`, {
            method: 'Patch',
            headers: getHeaders(),
            body: JSON.stringify(data),
        }).then((res) => handleResponse<T>(res)),

    delete: (endpoint: string) =>
        fetch(`${API_URL}${endpoint}`, { method: 'DELETE' }).then((res) => handleResponse(res)),
};
