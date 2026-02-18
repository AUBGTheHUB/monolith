import { Button } from '@/components/ui/button.tsx';
import { Card } from '@/components/ui/card.tsx';
import { AdminCard } from '@/internalLibrary/AdminCard/adminCard.tsx';
import { cn } from '@/lib/utils.ts';
import { apiClient } from '@/services/apiClient.ts';
import type { Mentor } from '@/types/mentor.ts';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Fragment, useEffect } from 'react';
import { Helmet } from 'react-helmet';
import { Link } from 'react-router';
import { Styles } from '../../../AdminStyle.ts';
import { MentorsPageMessages as MESSAGES } from './messages.tsx';

export function MentorsListPage() {
    const queryClient = useQueryClient();

    // Fetch
    const { data, isLoading, error, isError } = useQuery({
        queryKey: ['mentors', 'list'],
        queryFn: () => apiClient.get<{ mentors: Mentor[] }>('/admin/mentors'),
        select: (res) => res.mentors,
    });

    useEffect(() => {
        if (isError) {
            console.error(error);
            alert(error);
        }
    });

    const deleteMutation = useMutation({
        mutationFn: (id: string) => apiClient.delete(`/admin/mentors/${id}`),
        onSuccess: async () => {
            await queryClient.invalidateQueries({ queryKey: ['mentors', 'list'] });
        },
        onError: (error) => alert(error.message),
    });

    const handleDelete = (id: string, name: string) => {
        if (window.confirm(MESSAGES.DELETE_CONFIRM(name))) {
            deleteMutation.mutate(id);
        }
    };

    const renderMentorActions = (mentorId: string, mentorName: string) => (
        <div className="flex gap-3 w-full">
            <Link to={`/admin/dashboard/mentors/${mentorId}`} className="flex-1">
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
                onClick={() => handleDelete(mentorId, mentorName)}
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

                            <Link to="/admin/dashboard/mentors/add">
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

                        <Link to="/admin/dashboard/mentors/add">
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
                            {data.map((mentor) => (
                                <div key={mentor.id} className="group">
                                    <AdminCard
                                        imageUrl={mentor.avatar_url}
                                        imageAlt={mentor.name}
                                        title={mentor.name}
                                        subtitle={mentor.company}
                                        position={mentor.job_title}
                                        linkedinUrl={mentor.linkedin_url}
                                        actions={renderMentorActions(mentor.id, mentor.name)}
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
