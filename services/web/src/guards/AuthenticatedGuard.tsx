import { useAuthStore } from '@/hooks/useAuthStore';
import { Outlet, Navigate } from 'react-router';

interface AuthGuardProps {
    isAuth: boolean;
}
export const AuthenticatedGuard = ({ isAuth }: AuthGuardProps) => {
    const accessToken = useAuthStore((state) => state.accessToken);
    if (!accessToken && isAuth) {
        return <Navigate to="/auth/login" replace />;
    }
    if (accessToken && !isAuth) {
        return <Navigate to="/admin/dashboard" replace />;
    }
    return <Outlet />;
};
