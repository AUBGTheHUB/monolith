import { User } from '@/types/auth';
import { create } from 'zustand';

type AuthState = {
    accessToken: string | null;
    idToken: string | null;
    user: User | null;
    setAuth: (accessToken: string, idToken: string, user: User) => void;
    setNewAuthToken: (accessToken: string) => void;
    clearAuth: () => void;
};

export const useAuthStore = create<AuthState>((set) => ({
    accessToken: null,
    idToken: null,
    user: null,
    setAuth: (accessToken: string, idToken: string, user: User) =>
        set({ accessToken: accessToken, idToken: idToken, user: user }),
    setNewAuthToken: (accessToken: string) => set({ accessToken: accessToken }),
    clearAuth: () => set({ accessToken: null, idToken: null, user: null }),
}));
