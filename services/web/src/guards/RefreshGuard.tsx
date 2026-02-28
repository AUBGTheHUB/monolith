import { useState, useEffect } from 'react';
import { Navigate, Outlet } from 'react-router';
import { refreshToken } from '@/services/refreshToken.ts';

export const RefreshGuard = () => {
    const [status, setStatus] = useState<'loading' | 'auth' | 'error'>('loading');

    useEffect(() => {
        const initialRefresh = async () => {
            try {
                await refreshToken();
                setStatus('auth');
            } catch (err) {
                console.error('Refresh failed', err);
                setStatus('error');
            }
        };

        initialRefresh();
    }, []);

    // 1. Handle the "Waiting" state
    if (status === 'loading') {
        return (
            <div className="flex items-center justify-center min-h-screen bg-slate-950">
                <div className="text-white animate-pulse">Verifying session...</div>
            </div>
        );
    }

    // 2. Handle the "Failed" state
    if (status === 'error') {
        return <Navigate to="/admin/login" replace />;
    }

    // 3. Handle the "Success" state
    return <Outlet />;
};
