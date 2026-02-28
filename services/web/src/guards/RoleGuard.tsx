import { useAuthStore } from '@/hooks/useAuthStote';
import { Outlet, Navigate } from 'react-router';

interface RoleGuardProps {
    allowedRoles: string[];
}

export const RoleGuard = ({ allowedRoles }: RoleGuardProps) => {
    const siteRole = useAuthStore.getState().user?.siteRole;
    if (!siteRole) {
        return <Navigate to="/admin/login" replace />;
    }
    if (!allowedRoles.includes(siteRole)) {
        return <Navigate to="/admin/forbidden" replace />;
    }
    return <Outlet />;
};
