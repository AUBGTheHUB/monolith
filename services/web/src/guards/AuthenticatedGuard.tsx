import { useAuthStore } from '@/hooks/useAuthStore';
import { Outlet, Navigate } from 'react-router';

interface AuthGuardProps {
    isAuth: boolean;
}
export const AuthenticatedGuard = ({ isAuth }: AuthGuardProps) => {
    const access_token = useAuthStore.getState().accessToken;

    if (!access_token && isAuth) {
        return <Navigate to="/auth/login" replace />;
    }
    if (access_token && !isAuth) {
        return <Navigate to="/admin/forbidden" replace />;
    }
    return <Outlet />;
};
