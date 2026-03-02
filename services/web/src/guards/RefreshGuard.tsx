import { useState, useEffect } from 'react';
import { Navigate, Outlet } from 'react-router';
import { refreshToken } from '@/services/refreshToken.ts';
import { useAuthStore } from '@/hooks/useAuthStore';

export const RefreshGuard = () => {
    const [status, setStatus] = useState<'loading' | 'auth' | 'error'>('loading');

    useEffect(() => {
        const initialRefresh = async () => {
            if (useAuthStore.getState().accessToken) {
                setStatus('auth');
            } else {
                try {
                    await refreshToken();
                    setStatus('auth');
                } catch {
                    setStatus('error');
                }
            }
        };

        initialRefresh();
    }, []);

    if (status === 'loading') {
        return (
            <div className="flex items-center justify-center min-h-screen bg-slate-950">
                <div className="text-white animate-pulse">Verifying session...</div>
            </div>
        );
    }

    if (status === 'error') {
        return <Navigate to="/admin/login" replace />;
    }

    return <Outlet />;
};
