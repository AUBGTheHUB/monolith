import { User } from '@/types/auth';
import { create } from 'zustand';
import { refreshToken } from '@/services/refreshToken.ts';

type AuthState = {
    accessToken: string | null;
    idToken: string | null;
    user: User | null;
    isInitialized: boolean;
    setAuth: (accessToken: string, idToken: string, user: User) => void;
    clearAuth: () => void;
    initialize: () => Promise<void>;
};

export const useAuthStore = create<AuthState>((set, get) => ({
    accessToken: null,
    idToken: null,
    user: null,
    isInitialized: false,

    setAuth: (accessToken: string, idToken: string, user: User) =>
        set({ accessToken, idToken, user, isInitialized: true }),

    clearAuth: () => set({ accessToken: null, idToken: null, user: null }),

    initialize: async () => {
        // Prevent double initialization if already authenticated
        if (get().accessToken) {
            set({ isInitialized: true });
            return;
        }

        try {
            // Attempt to get a new token from the HttpOnly cookie
            await refreshToken();
        } catch (error) {
            console.error('Session restoration failed:', error);
        } finally {
            set({ isInitialized: true });
        }
    },
}));
