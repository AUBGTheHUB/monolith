import { refreshToken } from '@/services/refreshToken';
import { useEffect, useState } from 'react';
import { Navigate, Outlet } from 'react-router';

export const RefreshGuard = () => {
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        const initialRefresh = async () => {
            try {
                await refreshToken();
            } catch {
                return <Navigate to="/admin/login" replace />;
            } finally {
                setLoading(false);
            }
        };

        initialRefresh();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    return <Outlet />;
};
