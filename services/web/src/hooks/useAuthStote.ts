import { create } from 'zustand';

type AuthState = {
    accessToken: string | null;
    setAuth: (token: string) => void;
    clearAuth: () => void;
};

export const useAuthStore = create<AuthState>((set) => ({
    accessToken: null,
    setAuth: (token: string) => set({ accessToken: token }),
    clearAuth: () => set({ accessToken: null }),
}));
