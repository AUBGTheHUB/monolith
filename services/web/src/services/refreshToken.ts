import { API_URL } from '@/constants';
import { useAuthStore } from '@/hooks/useAuthStore';
import { User } from '@/types/auth';
import { jwtDecode } from 'jwt-decode';

let refreshPromise: Promise<void> | null = null;

export const refreshToken = async (): Promise<void> => {
    if (refreshPromise) return refreshPromise;

    refreshPromise = (async () => {
        try {
            const refreshResponse = await fetch(`${API_URL}/auth/refresh`, {
                method: 'POST',
                credentials: 'include',
            });

            // NOTE: fetch doesn't throw on 401/500, so we must check ok status
            if (!refreshResponse.ok) {
                useAuthStore.getState().clearAuth();
                return;
            }

            const refreshData = await refreshResponse.json();

            const user = jwtDecode<User>(refreshData.id_token);

            // Update the store
            useAuthStore.getState().setAuth(refreshData.access_token, refreshData.id_token, user);
        } catch (err) {
            // Clear auth so the app knows we are definitely logged out
            useAuthStore.getState().clearAuth();
            throw err;
        } finally {
            refreshPromise = null;
        }
    })();

    return refreshPromise;
};
