import { useAuthStore } from '@/hooks/useAuthStote';
import { Outlet, Navigate } from 'react-router';

interface AuthGuardProps {
    isAuth: boolean;
}
export const AuthenticatedGuard = ({ isAuth }: AuthGuardProps) => {
    const user = useAuthStore.getState().user;

    if (!user && isAuth) {
        return <Navigate to="/admin/login" replace />;
    }
    if (user && !isAuth) {
        return <Navigate to="/admin/forbidden" replace />;
    }
    return <Outlet />;
};
