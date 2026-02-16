import { Fragment, useEffect } from 'react';
import { Link } from 'react-router';
import { Judge } from '@/types/judge.ts';
import { AdminCard } from '@/internalLibrary/AdminCard/adminCard.tsx';
import { Card } from '@/components/ui/card.tsx';
import { Button } from '@/components/ui/button.tsx';
import { Helmet } from 'react-helmet';
import { JudgesPageMessages as MESSAGES } from './messages.tsx';
import { Styles } from '../../../AdminStyle.ts';
import { cn } from '@/lib/utils.ts';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/services/apiClient.ts';

export function JudgesListPage() {
    const queryClient = useQueryClient();
    // Fetch
    const { data, isLoading, error, isError } = useQuery({
        queryKey: ['judges'],
        queryFn: () => apiClient.get<{ judges: Judge[] }>('/admin/judges'),
        select: (res) => res.judges,
    });
    useEffect(() => {
        if (isError) {
            console.error(error);
            alert(error);
        }
    });

    const deleteMutation = useMutation({
        mutationFn: (id: string) => apiClient.delete(`/admin/judges/${id}`),
        onSuccess: async () => {
            await queryClient.invalidateQueries({ queryKey: ['judges'] });
        },
        onError: (error) => alert(error.message),
    });

    const handleDelete = (id: string, name: string) => {
        if (window.confirm(MESSAGES.DELETE_CONFIRM(name))) {
            deleteMutation.mutate(id);
        }
    };

    const renderJudgeActions = (judgeId: string, judgeName: string) => (
        <div className="flex gap-3 w-full">
            <Link to={`/admin/dashboard/judges/${judgeId}`} className="flex-1">
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
                onClick={() => handleDelete(judgeId, judgeName)}
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

                            <Link to="/admin/dashboard/judges/add">
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

                        <Link to="/admin/dashboard/judges/add">
                            <Button
                                size="lg"
                                style={{ backgroundColor: Styles.colors.hubCyan }}
                                className={cn('px-8 py-6 text-lg', Styles.actions.primaryButton)}
                            >
                                {MESSAGES.ADD_BUTTON}
                            </Button>
                        </Link>
                    </div>

                    {!data || data.length === 0 ? (
                        <Card className={cn('p-20 text-center border-dashed', Styles.glass.card)}>
                            <p className={cn('text-xl font-medium', Styles.text.subtitle)}>{MESSAGES.EMPTY_STATE}</p>
                        </Card>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                            {data.map((judge) => (
                                <div key={judge.id} className="group">
                                    <AdminCard
                                        imageUrl={judge.avatar_url}
                                        imageAlt={judge.name}
                                        title={judge.name}
                                        subtitle={judge.company}
                                        position={judge.job_title}
                                        linkedinUrl={judge.linkedin_url}
                                        actions={renderJudgeActions(judge.id, judge.name)}
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
