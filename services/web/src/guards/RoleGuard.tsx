import { useAuthStore } from '@/hooks/useAuthStore';
import { Outlet, Navigate } from 'react-router';

interface RoleGuardProps {
    allowedRoles: string[];
}

export const RoleGuard = ({ allowedRoles }: RoleGuardProps) => {
    const siteRole = useAuthStore((state) => state.user?.site_role);
    if (!siteRole) {
        return <Navigate to="/auth/login" replace />;
    }
    if (!allowedRoles.includes(siteRole)) {
        return <Navigate to="/admin/forbidden" replace />;
    }
    return <Outlet />;
};
