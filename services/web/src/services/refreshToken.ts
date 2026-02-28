import { API_URL } from '@/constants';
import { useAuthStore } from '@/hooks/useAuthStote';

let refreshPromise: Promise<void> | null = null;

export const refreshToken = async (): Promise<void> => {
    if (refreshPromise) {
        //For when multiple tabs are open, if currently refreshing it won't refresh again
        return refreshPromise;
    }

    refreshPromise = (async () => {
        try {
            const refreshResponse = await fetch(`${API_URL}/auth/refresh`, { method: 'POST', credentials: 'include' });
            const refreshData = await refreshResponse.json();
            useAuthStore.getState().setNewAuthToken(refreshData.access_token);
        } catch (err) {
            useAuthStore.getState().clearAuth();
            throw err;
        } finally {
            refreshPromise = null;
        }
    })();

    return refreshPromise;
};
