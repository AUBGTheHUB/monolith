import { Fragment } from 'react/jsx-runtime';
import { Link, useNavigate } from 'react-router';
import { Button } from '@/components/ui/button';
import { Helmet } from 'react-helmet';
import { Styles } from '../AdminStyle';
import { cn } from '@/lib/utils';
import { useAuthStore } from '@/hooks/useAuthStore';
import { API_URL, ROLES } from '@/constants';
import { Home, LogOut } from 'lucide-react';
import AdminPageCard from '@/website/AdminPanelPage/DashboardPages/components/AdminPageCard.tsx';
import { useMutation } from '@tanstack/react-query';

export function DashboardPage() {
    const user = useAuthStore((state) => state.user);
    const siteRole = user?.site_role;
    const navigate = useNavigate();

    const mutation = useMutation({
        mutationFn: () => {
            return fetch(`${API_URL}/auth/logout`, { method: 'POST' });
        },
        onSuccess: async () => {
            navigate('/');
        },
        onError: (error: Error) => {
            alert(error.message);
        },
    });

    const handleLogout = () => {
        useAuthStore.getState().clearAuth();
        mutation.mutate();
    };

    return (
        <Fragment>
            <Helmet>
                <title>Admin Panel - The Hub AUBG</title>
            </Helmet>
            <div
                className={cn('min-h-screen p-4 md:p-8 flex flex-col items-center', Styles.backgrounds.primaryGradient)}
            >
                <div className="max-w-7xl w-full mx-auto">
                    {/* Integrated Header & Navigation */}
                    <div className="flex flex-col md:flex-row md:justify-between md:items-end gap-6 mb-16 border-b border-white/10 pb-8">
                        <div>
                            <h1 className={cn('text-4xl md:text-5xl text-left', Styles.text.title)}>
                                Admin <span style={{ color: Styles.colors.hubCyan }}>Panel</span>
                            </h1>
                            <div className="mt-2 flex items-center gap-2">
                                <span className="px-3 py-1 rounded-full bg-white/10 text-xs font-mono uppercase tracking-wider text-white">
                                    Role: {siteRole || 'Guest'}
                                </span>
                            </div>
                        </div>

                        <div className="flex flex-wrap items-center gap-3">
                            <span className="text-white/70 mr-2 hidden sm:inline-block">
                                Welcome, <strong>{user?.username}</strong>
                            </span>
                            <Link to="/">
                                <Button
                                    variant="outline"
                                    className="gap-2 bg-white/5 border-white/20 text-white hover:bg-white/10"
                                >
                                    <Home size={18} /> Home
                                </Button>
                            </Link>
                            <Button
                                onClick={handleLogout}
                                variant="destructive"
                                className="gap-2 bg-red-500/80 hover:bg-red-600"
                            >
                                <LogOut size={18} /> Logout
                            </Button>
                        </div>
                    </div>

                    {/* Dashboard Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {/* Developer/SuperAdmin Only */}
                        {(siteRole === ROLES.dev || siteRole === ROLES.superAdmin) && (
                            <AdminPageCard title="Feature Switches" link="/admin/dashboard/feature-switches" />
                        )}

                        {/* Board/SuperAdmin Only */}
                        {(siteRole === ROLES.board || siteRole === ROLES.superAdmin) && (
                            <>
                                <AdminPageCard title="Judges" link="/admin/dashboard/judges" />
                                <AdminPageCard title="Sponsors" link="/admin/dashboard/sponsors" />
                                <AdminPageCard title="Meet The Team" link="/admin/dashboard/meet-the-team" />
                                <AdminPageCard title="Mentors" link="/admin/dashboard/mentors" />
                                <AdminPageCard title="Past Events" link="/admin/dashboard/past-events" />
                            </>
                        )}
                    </div>
                </div>
            </div>
        </Fragment>
    );
}
