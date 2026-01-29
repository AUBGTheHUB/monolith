import { API_URL } from '../constants.ts';

const getHeaders = (contentType?: string) => {
    const headers: HeadersInit = {
        // Shared headers
        Authorization: 'Bearer a0e923d30b613ce5cf57d9af35a3d4d2e8efa660f579b9a547918bd1c83fdb7b',
    };

    // Only add Content-Type if we are actually sending data
    if (contentType) {
        headers['Content-Type'] = contentType;
    }

    return headers;
};

const handleResponse = async <T>(response: Response): Promise<T> => {
    if (!response.ok) {
        const error = await response.json().catch(() => ({ message: 'An unexpected error occurred' }));
        throw new Error(error.message || `Error: ${response.status}`);
    }

    // Return empty object for 204 No Content, otherwise parse JSON
    if (response.status === 204) return {} as T;

    return response.json();
};

export const apiClient = {
    // GET and DELETE don't need Content-Type headers
    get: <T>(endpoint: string) =>
        fetch(`${API_URL}${endpoint}`, {
            method: 'GET',
            headers: getHeaders(),
        }).then((res) => handleResponse<T>(res)),

    delete: (endpoint: string) =>
        fetch(`${API_URL}${endpoint}`, {
            method: 'DELETE',
            headers: getHeaders(),
        }).then((res) => handleResponse(res)),

    // POST and PATCH require the JSON content-type
    post: <T, D>(endpoint: string, data: D) =>
        fetch(`${API_URL}${endpoint}`, {
            method: 'POST',
            headers: getHeaders('application/json'),
            body: JSON.stringify(data),
        }).then((res) => handleResponse<T>(res)),

    patch: <T, D>(endpoint: string, data: D) =>
        fetch(`${API_URL}${endpoint}`, {
            method: 'PATCH',
            headers: getHeaders('application/json'),
            body: JSON.stringify(data),
        }).then((res) => handleResponse<T>(res)),
};
