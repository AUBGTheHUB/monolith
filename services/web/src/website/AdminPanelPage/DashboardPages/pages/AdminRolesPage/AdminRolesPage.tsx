import { Fragment, useEffect, useState } from 'react';
import { Link } from 'react-router';
import { Helmet } from 'react-helmet';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Styles } from '../../../AdminStyle';
import { cn } from '@/lib/utils';
import { apiClient } from '@/services/apiClient';
import type { AdminUser } from '@/types/admin';
import { AdminRolesMessages as MESSAGES } from './messages';
import { AdminRoleRow, AdminRole } from './components/AdminRoleRow';

type UpdateRolePayload = {
    site_role: AdminRole;
};

export function AdminRolesPage() {
    const queryClient = useQueryClient();
    const [updatingId, setUpdatingId] = useState<string | null>(null);

    const { data, isLoading, isError, error } = useQuery({
        queryKey: ['admins', 'list'],
        queryFn: () => apiClient.get<{ admins: AdminUser[] }>('/users'),
        select: (res) => res.admins,
    });

    useEffect(() => {
        if (isError) {
            alert(error);
        }
    }, [isError, error]);

    const mutation = useMutation({
        mutationFn: ({ id, role }: { id: string; role: AdminRole }) => {
            const payload: UpdateRolePayload = { site_role: role };
            return apiClient.patch<undefined, UpdateRolePayload>(`/users/${id}/role`, payload);
        },
        onSuccess: async () => {
            await queryClient.invalidateQueries({ queryKey: ['admins'] });
            setUpdatingId(() => null);
        },
        onError: (error) => {
            alert(error.message);
            setUpdatingId(() => null);
        },
    });

    const handleChangeRole = (id: string, newRole: AdminRole) => {
        setUpdatingId(() => id);
        mutation.mutate({ id, role: newRole });
    };

    const admins = data || [];

    const content = (() => {
        if (isLoading) {
            return (
                <Card className={cn('p-8 space-y-4', Styles.glass.card)}>
                    <p className={cn('text-base md:text-lg', Styles.text.subtitle)}>{MESSAGES.LOADING_STATE}</p>
                    <div className="space-y-3">
                        {[1, 2, 3].map((i) => (
                            <div key={i} className="h-12 rounded-xl bg-white/5 animate-pulse" />
                        ))}
                    </div>
                </Card>
            );
        }

        if (!admins.length) {
            return (
                <Card className={cn('p-20 text-center border-dashed', Styles.glass.card)}>
                    <p className={cn('text-xl font-medium', Styles.text.subtitle)}>{MESSAGES.EMPTY_STATE}</p>
                </Card>
            );
        }

        return (
            <Card className={cn('p-6 md:p-8 space-y-4', Styles.glass.card)}>
                <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-white/70">Admins</span>
                    <span className="text-xs text-white/50">{admins.length} total</span>
                </div>
                <div className="space-y-3">
                    {admins.map((admin) => (
                        <AdminRoleRow
                            key={admin.id}
                            admin={admin}
                            isUpdating={updatingId === admin.id}
                            onChangeRole={(role) => handleChangeRole(admin.id, role)}
                        />
                    ))}
                </div>
            </Card>
        );
    })();

    return (
        <Fragment>
            <Helmet>
                <title>{MESSAGES.PAGE_TITLE}</title>
            </Helmet>

            <div className={cn('min-h-screen p-8', Styles.backgrounds.primaryGradient)}>
                <div className="max-w-5xl mx-auto">
                    <Link to="/admin/dashboard">
                        <Button variant="ghost" className={cn('mb-6', Styles.glass.ghostButton)}>
                            {MESSAGES.BACK_BUTTON}
                        </Button>
                    </Link>

                    <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-10">
                        <div>
                            <h1 className={cn('text-4xl', Styles.text.title)}>{MESSAGES.HEADING}</h1>
                            <p className={Styles.text.subtitle}>{MESSAGES.SUBTITLE}</p>
                        </div>
                    </div>

                    {content}
                </div>
            </div>
        </Fragment>
    );
}
