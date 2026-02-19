import { API_URL } from '../constants.ts';
import { useAuthStore } from '@/hooks/useAuthStote.ts';
import { refreshToken } from './refreshToken.ts';

const getHeaders = (contentType?: string) => {
    const headers: HeadersInit = {};

    const accessToken = useAuthStore.getState().accessToken;
    if (accessToken) {
        headers['Authorization'] = `Bearer ${accessToken}`;
    }

    // Only add Content-Type if we are actually sending data
    if (contentType) {
        headers['Content-Type'] = contentType;
    }

    return headers;
};

const handleResponse = async <R>(response: Response, originalRequest: () => Promise<Response>): Promise<R> => {
    //Handle responses based on FastAPI's response schemas
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
    //Unathorized
    if (response.status == 401 && !response.url.includes('login')) {
        try {
            await refreshToken();
            const retryResponse = await originalRequest();
            return handleResponse<R>(retryResponse, () => Promise.reject('Retry failed'));
        } catch (err) {
            alert(err);
        }
    }
    if (response.status == 400 || response.status == 404) {
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
    get: <R>(endpoint: string) => {
        const req = () => fetch(`${API_URL}${endpoint}`, { method: 'GET', headers: getHeaders() });
        return req().then((res) => handleResponse<R>(res, req));
    },

    delete: (endpoint: string) => {
        const req = () => fetch(`${API_URL}${endpoint}`, { method: 'DELETE', headers: getHeaders() });
        return req().then((res) => handleResponse(res, req));
    },

    // POST and PATCH require the JSON content-type
    post: <R, D>(endpoint: string, data: D) => {
        const req = () =>
            fetch(`${API_URL}${endpoint}`, {
                method: 'POST',
                headers: getHeaders('application/json'),
                body: JSON.stringify(data),
            });
        return req().then((res) => handleResponse<R>(res, req));
    },

    patch: <R, D>(endpoint: string, data: D) => {
        const req = () =>
            fetch(`${API_URL}${endpoint}`, {
                method: 'PATCH',
                headers: getHeaders('application/json'),
                body: JSON.stringify(data),
            });
        return req().then((res) => handleResponse<R>(res, req));
    },
};
