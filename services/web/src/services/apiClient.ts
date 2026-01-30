import { API_URL } from '../constants.ts';

const getHeaders = (contentType?: string) => {
    const headers: HeadersInit = {
        // Shared headers
        //TEMP SOLUTION: Will change when auth is implemented
        Authorization: 'Bearer a0e923d30b613ce5cf57d9af35a3d4d2e8efa660f579b9a547918bd1c83fdb7b',
    };

    // Only add Content-Type if we are actually sending data
    if (contentType) {
        headers['Content-Type'] = contentType;
    }

    return headers;
};

const handleResponse = async <R>(response: Response): Promise<R> => {
    if (response.status == 204) {
        return {} as R;
    }
    if (response.status == 422) {
        //Here server returns the verification members under msg
        const errorData = await response.json();
        const messages = errorData.detail
            .map((e: { loc: string[]; msg: string }) => {
                const field = e.loc?.slice(1).join('.') ?? 'field';
                return `${field}: ${e.msg}`;
            })
            .join('\n');

        throw new Error(messages);
    }
    if (response.status == 400 || response.status == 401 || response.status == 404) {
        const errorData = await response.json();
        const message = errorData.error || 'Unexpected error occurred!';
        throw new Error(message);
    }
    if (!response.ok) {
        throw new Error('Unexpected error occurred. Contact TheHub.');
    }
    return response.json();
};

export const apiClient = {
    // GET and DELETE don't need Content-Type headers
    get: <R>(endpoint: string) =>
        fetch(`${API_URL}${endpoint}`, {
            method: 'GET',
            headers: getHeaders(),
        }).then((res) => handleResponse<R>(res)),

    delete: (endpoint: string) =>
        fetch(`${API_URL}${endpoint}`, {
            method: 'DELETE',
            headers: getHeaders(),
        }).then((res) => handleResponse(res)),

    // POST and PATCH require the JSON content-type
    post: <R, D>(endpoint: string, data: D) =>
        fetch(`${API_URL}${endpoint}`, {
            method: 'POST',
            headers: getHeaders('application/json'),
            body: JSON.stringify(data),
        }).then((res) => handleResponse<R>(res)),

    patch: <R, D>(endpoint: string, data: D) =>
        fetch(`${API_URL}${endpoint}`, {
            method: 'PATCH',
            headers: getHeaders('application/json'),
            body: JSON.stringify(data),
        }).then((res) => handleResponse<R>(res)),
};
