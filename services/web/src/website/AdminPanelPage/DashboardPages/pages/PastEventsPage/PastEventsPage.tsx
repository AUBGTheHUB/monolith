import { useEffect } from 'react';
import { Link } from 'react-router';
import { PastEvent } from '@/types/past-events.ts';
import { Card } from '@/components/ui/card.tsx';
import { AdminCard } from '@/internalLibrary/AdminCard/adminCard.tsx';
import { Button } from '@/components/ui/button.tsx';
import { Helmet } from 'react-helmet';
import { Styles } from '../../../AdminStyle.ts';
import { PastEventsPageMessages as MESSAGES } from './messages.tsx';
import { cn } from '@/lib/utils.ts';
import { apiClient } from '@/services/apiClient.ts';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

export function PastEventsPage() {
    const queryClient = useQueryClient();
    // Fetch
    const { data, isLoading, error, isError } = useQuery({
        queryKey: ['events'],
        queryFn: () => apiClient.get<{ past_events: PastEvent[] }>('/admin/events'),
        select: (res) => res.past_events,
    });
    useEffect(() => {
        if (isError) {
            console.error(error);
            alert(error);
        }
    }, [isError, error]);

    // Delete
    const deleteMutation = useMutation({
        mutationFn: (id: string) => apiClient.delete(`/admin/events/${id}`),
        onSuccess: async () => {
            await queryClient.invalidateQueries({ queryKey: ['events'] });
        },
        onError: (error) => alert(error.message),
    });

    const handleDelete = (id: string, name: string) => {
        if (window.confirm(MESSAGES.DELETE_CONFIRM(name))) {
            deleteMutation.mutate(id);
        }
    };

    const renderEventActions = (eventId: string, eventName: string) => (
        <div className="flex gap-3 w-full">
            <Link to={`/admin/dashboard/past-events/${eventId}`} className="flex-1">
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
                onClick={() => handleDelete(eventId, eventName)}
            >
                {MESSAGES.DELETE_BUTTON}
            </Button>
        </div>
    );
    if (isLoading) {
        return (
            <>
                <Helmet>
                    <title>{MESSAGES.PAGE_TITLE}</title>
                </Helmet>

                <div className={cn('min-h-screen p-8', Styles.backgrounds.primaryGradient)}>
                    <div className="max-w-7xl mx-auto">
                        {/* Back */}
                        <Link to="/admin/dashboard">
                            <Button variant="ghost" className={cn('mb-6', Styles.glass.ghostButton)}>
                                {MESSAGES.BACK_BUTTON}
                            </Button>
                        </Link>

                        {/* Header */}
                        <div className="flex justify-between items-center mb-12">
                            <div>
                                <h1 className={cn('text-4xl', Styles.text.title)}>{MESSAGES.HEADING}</h1>
                                <p className={Styles.text.subtitle}>{MESSAGES.SUBTITLE}</p>
                            </div>

                            <Link to="/admin/dashboard/past-events/add">
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
            </>
        );
    }

    if (!isLoading) {
        return (
            <>
                <Helmet>
                    <title>{MESSAGES.PAGE_TITLE}</title>
                </Helmet>

                <div className={cn('min-h-screen p-8', Styles.backgrounds.primaryGradient)}>
                    <div className="max-w-7xl mx-auto">
                        {/* Back */}
                        <Link to="/admin/dashboard">
                            <Button variant="ghost" className={cn('mb-6', Styles.glass.ghostButton)}>
                                {MESSAGES.BACK_BUTTON}
                            </Button>
                        </Link>

                        {/* Header */}
                        <div className="flex justify-between items-center mb-12">
                            <div>
                                <h1 className={cn('text-4xl', Styles.text.title)}>{MESSAGES.HEADING}</h1>
                                <p className={Styles.text.subtitle}>{MESSAGES.SUBTITLE}</p>
                            </div>

                            <Link to="/admin/dashboard/past-events/add">
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
                                <p className={cn('text-xl font-medium', Styles.text.subtitle)}>
                                    {MESSAGES.EMPTY_STATE}
                                </p>
                            </Card>
                        ) : (
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                                {data.map((event) => (
                                    <AdminCard
                                        key={event.id}
                                        imageUrl={event.cover_picture}
                                        imageAlt="No Event Image"
                                        title={event.title}
                                        {...(event.tags?.length ? { subtitle: event.tags.join(', ') } : {})}
                                        actions={renderEventActions(event.id, event.title)}
                                        className={Styles.glass.card}
                                    />
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </>
        );
    }
}
