import { API_URL } from '@/constants';
import { useAuthStore } from '@/hooks/useAuthStore';
import { User } from '@/types/auth';
import { jwtDecode } from 'jwt-decode';

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
            const user = jwtDecode<User>(refreshData.id_token);
            useAuthStore.getState().setAuth(refreshData.access_token, refreshData.id_token, user);
        } catch (err) {
            useAuthStore.getState().clearAuth();
            throw err;
        } finally {
            refreshPromise = null;
        }
    })();

    return refreshPromise;
};
