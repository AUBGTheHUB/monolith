import { refreshToken } from '@/services/refreshToken';
import { ReactNode, useEffect, useState } from 'react';
import { useNavigate } from 'react-router';

interface RefreshProviderProps {
    children: ReactNode;
}
export const RefreshProvider = ({ children }: RefreshProviderProps) => {
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();
    useEffect(() => {
        const initialRefresh = async () => {
            try {
                await refreshToken();
            } catch {
                navigate('/login');
            } finally {
                setLoading(false);
            }
        };

        initialRefresh();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    return <>{children}</>;
};
