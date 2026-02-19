import { API_URL } from '@/constants';
import { useAuthStore } from '@/hooks/useAuthStote';

let refreshPromise: Promise<void> | null = null;

export const refreshToken = async (): Promise<void> => {
    if (refreshPromise) {
        return refreshPromise;
    }

    refreshPromise = (async () => {
        try {
            const refreshResponse = await fetch(`${API_URL}/auth/refresh`, { method: 'POST', credentials: 'include' });
        } catch (err) {
            useAuthStore.getState().clearAuth();
            throw err;
        } finally {
            refreshPromise = null;
        }

        const refreshData = await refreshResponse.json();
        useAuthStore.getState().setAuth(refreshData.accessToken);
    })();

    return refreshPromise;
};
