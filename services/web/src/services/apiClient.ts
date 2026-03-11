import { API_URL } from '../constants.ts';
import { useAuthStore } from '@/hooks/useAuthStore';
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

const handleResponse = async <R>(
    response: Response,
    originalRequest: () => Promise<Response>,
    hasTriedRefresh: boolean,
): Promise<R> => {
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
    //Unauthorized
    if (response.status == 401 && !response.url.includes('login')) {
        if (hasTriedRefresh) {
            throw new Error('Expired session. Log in again.');
        }
        await refreshToken();
        const retryResponse = await originalRequest();
        return handleResponse<R>(retryResponse, () => Promise.reject('Retry failed'), true);
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
    get: async <R>(endpoint: string): Promise<R> => {
        const req = () => fetch(`${API_URL}${endpoint}`, { method: 'GET', headers: getHeaders() });
        const res = await req();
        return handleResponse<R>(res, req, false);
    },

    delete: async <R>(endpoint: string): Promise<R> => {
        const req = () => fetch(`${API_URL}${endpoint}`, { method: 'DELETE', headers: getHeaders() });
        const res = await req();
        return handleResponse<R>(res, req, false);
    },

    post: async <R, D>(endpoint: string, data: D): Promise<R> => {
        const req = () =>
            fetch(`${API_URL}${endpoint}`, {
                method: 'POST',
                headers: getHeaders('application/json'),
                body: JSON.stringify(data),
            });
        const res = await req();
        return handleResponse<R>(res, req, false);
    },

    patch: async <R, D>(endpoint: string, data: D): Promise<R> => {
        const req = () =>
            fetch(`${API_URL}${endpoint}`, {
                method: 'PATCH',
                headers: getHeaders('application/json'),
                body: JSON.stringify(data),
            });
        const res = await req();
        return handleResponse<R>(res, req, false);
    },

    postForm: async <R>(endpoint: string, formData: FormData): Promise<R> => {
        const req = () =>
            fetch(`${API_URL}${endpoint}`, {
                method: 'POST',
                headers: getHeaders(),
                body: formData,
            });
        const res = await req();
        return handleResponse<R>(res, req, false);
    },

    patchForm: async <R>(endpoint: string, formData: FormData): Promise<R> => {
        const req = () =>
            fetch(`${API_URL}${endpoint}`, {
                method: 'PATCH',
                headers: getHeaders(),
                body: formData,
            });
        const res = await req();
        return handleResponse<R>(res, req, false);
    },
};
