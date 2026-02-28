import { Fragment, useEffect } from 'react';
import { Link } from 'react-router';
import { AdminCard } from '@/internalLibrary/AdminCard/adminCard.tsx';
import { Card } from '@/components/ui/card.tsx';
import { Button } from '@/components/ui/button.tsx';
import { Helmet } from 'react-helmet';
import { TeamPageMessages as MESSAGES } from './messages.tsx';
import { Styles } from '../../../AdminStyle.ts';
import { cn } from '@/lib/utils.ts';
import { apiClient } from '@/services/apiClient.ts';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { BaseHubMember } from '@/types/hub-member.ts';

export function MeetTheTeamPage() {
    const queryClient = useQueryClient();

    // 1. Fetching Logic
    const { data, isLoading, error, isError } = useQuery({
        queryKey: ['hub-members'],
        queryFn: () => apiClient.get<{ members: BaseHubMember[] }>('/admin/hub-members'),
        select: (res) => res.members,
    });

    useEffect(() => {
        if (isError) {
            console.error(error);
            alert(error instanceof Error ? error.message : 'Failed to fetch members');
        }
    }, [isError, error]);

    // 2. Deletion Logic (Mutation)
    const deleteMutation = useMutation({
        mutationFn: (id: string) => apiClient.delete(`/admin/hub-members/${id}`),
        onSuccess: async () => {
            await queryClient.invalidateQueries({ queryKey: ['hub-members'] });
        },
        onError: (error: Error) => alert(error.message),
    });

    const handleDelete = (id: string, name: string) => {
        if (window.confirm(MESSAGES.DELETE_CONFIRM(name))) {
            deleteMutation.mutate(id);
        }
    };

    const renderMemberActions = (id: string, name: string) => (
        <div className="flex gap-3 w-full">
            <Link to={`${id}`} className="flex-1">
                <Button
                    variant="outline"
                    className="w-full bg-white/5 border-white/10 text-white hover:bg-white/20 hover:text-white transition-all"
                >
                    {MESSAGES.EDIT_BUTTON}
                </Button>
            </Link>

            <Button
                variant="destructive"
                className="flex-1 shadow-lg shadow-red-500/10 hover:shadow-red-500/20 transition-all"
                onClick={() => handleDelete(id, name)}
            >
                {MESSAGES.DELETE_BUTTON}
            </Button>
        </div>
    );

    if (isLoading) {
        return (
            <Fragment>
                <Helmet>
                    <title>{MESSAGES.PAGE_TITLE}</title>
                </Helmet>

                <div className={cn('min-h-screen p-8', Styles.backgrounds.primaryGradient)}>
                    <div className="max-w-7xl mx-auto">
                        <Link to="/admin/dashboard">
                            <Button variant="ghost" className={cn('mb-6', Styles.glass.ghostButton)}>
                                {MESSAGES.BACK_BUTTON}
                            </Button>
                        </Link>

                        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-12">
                            <div>
                                <h1 className={cn('text-4xl', Styles.text.title)}>{MESSAGES.HEADING}</h1>
                                <p className={Styles.text.subtitle}>{MESSAGES.SUBTITLE}</p>
                            </div>

                            <Link to="add">
                                <Button
                                    size="lg"
                                    style={{ backgroundColor: Styles.colors.hubCyan }}
                                    className={cn('px-8 py-6 text-lg', Styles.actions.primaryButton)}
                                >
                                    {MESSAGES.ADD_BUTTON}
                                </Button>
                            </Link>
                        </div>

                        <Card className={cn('p-20 text-center border-dashed', Styles.glass.card)}>
                            <p className={cn('text-xl font-medium', Styles.text.subtitle)}>{MESSAGES.LOADING_STATE}</p>
                        </Card>
                    </div>
                </div>
            </Fragment>
        );
    }

    const members = data || [];

    return (
        <Fragment>
            <Helmet>
                <title>{MESSAGES.PAGE_TITLE}</title>
            </Helmet>

            <div className={cn('min-h-screen p-8', Styles.backgrounds.primaryGradient)}>
                <div className="max-w-7xl mx-auto">
                    <Link to="/admin/dashboard">
                        <Button variant="ghost" className={cn('mb-6', Styles.glass.ghostButton)}>
                            {MESSAGES.BACK_BUTTON}
                        </Button>
                    </Link>

                    <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-12">
                        <div>
                            <h1 className={cn('text-4xl', Styles.text.title)}>{MESSAGES.HEADING}</h1>
                            <p className={Styles.text.subtitle}>{MESSAGES.SUBTITLE}</p>
                        </div>

                        <Link to="add">
                            <Button
                                size="lg"
                                style={{ backgroundColor: Styles.colors.hubCyan }}
                                className={cn('px-8 py-6 text-lg', Styles.actions.primaryButton)}
                            >
                                {MESSAGES.ADD_BUTTON}
                            </Button>
                        </Link>
                    </div>

                    {members.length === 0 ? (
                        <Card className={cn('p-20 text-center border-dashed', Styles.glass.card)}>
                            <p className={cn('text-xl font-medium', Styles.text.subtitle)}>{MESSAGES.EMPTY_STATE}</p>
                        </Card>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                            {members.map((member) => (
                                <div key={member.id} className="group">
                                    <AdminCard
                                        imageUrl={member.avatar_url || ''}
                                        imageAlt={member.name}
                                        title={member.name}
                                        subtitle={member.position}
                                        position={
                                            member.departments.length > 0 ? member.departments.join(', ') : undefined
                                        }
                                        actions={renderMemberActions(member.id, member.name)}
                                        className={cn(
                                            'transition-all duration-300 group-hover:translate-y-[-4px]',
                                            Styles.glass.card,
                                            Styles.glass.cardHover,
                                            'rounded-2xl',
                                        )}
                                    />
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </Fragment>
    );
}
