import { Badge } from '@/components/ui/badge.tsx';
import { Button } from '@/components/ui/button.tsx';
import { Card } from '@/components/ui/card.tsx';
import { cn } from '@/lib/utils.ts';
import { apiClient } from '@/services/apiClient.ts';
import type { Attendee } from '@/types/attendee.ts';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Fragment, useEffect } from 'react';
import { Helmet } from 'react-helmet';
import { Link } from 'react-router';
import { Styles } from '../../../AdminStyle.ts';
import { AttendeesPageMessages as MESSAGES } from './messages.tsx';
import { ATTENDEES_ENDPOINT, ATTENDEES_QUERY_KEY, ATTENDEES_ROUTE, unwrapAttendees } from './constants.ts';

export function AttendeesPage() {
    const queryClient = useQueryClient();

    const { data, isLoading, error, isError } = useQuery({
        queryKey: [ATTENDEES_QUERY_KEY, 'list'],
        queryFn: () => apiClient.get<{ attendees: Attendee[] } | Attendee[]>(ATTENDEES_ENDPOINT),
        select: unwrapAttendees,
    });

    useEffect(() => {
        if (isError) {
            console.error(error);
            alert(error);
        }
    }, [isError, error]);

    const deleteMutation = useMutation({
        mutationFn: (id: string) => apiClient.delete(`${ATTENDEES_ENDPOINT}/${id}`),
        onSuccess: async () => {
            await queryClient.invalidateQueries({ queryKey: [ATTENDEES_QUERY_KEY] });
        },
        onError: (error) => alert(error.message),
    });

    const sendTicketMutation = useMutation({
        mutationFn: (attendee: Attendee) =>
            apiClient.post<unknown, { id: string }>(`${ATTENDEES_ENDPOINT}/send-ticket`, { id: attendee.id }),
        onSuccess: (_res, attendee) => alert(MESSAGES.SEND_TICKET_SUCCESS(attendee.name)),
        onError: (error) => alert(error.message),
    });

    const handleDelete = (attendee: Attendee) => {
        if (window.confirm(MESSAGES.DELETE_CONFIRM(attendee.name))) {
            deleteMutation.mutate(attendee.id);
        }
    };

    const handleSendTicket = (attendee: Attendee) => {
        if (window.confirm(MESSAGES.SEND_TICKET_CONFIRM(attendee.name, attendee.email))) {
            sendTicketMutation.mutate(attendee);
        }
    };

    const isSendingTicketFor = (id: string) => sendTicketMutation.isPending && sendTicketMutation.variables?.id === id;

    const header = (
        <Fragment>
            <Link to="/admin/dashboard">
                <Button variant="ghost" className={cn('mb-6', Styles.glass.ghostButton)}>
                    {MESSAGES.BACK_BUTTON}
                </Button>
            </Link>

            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-12">
                <div>
                    <h1 className={cn('text-3xl md:text-4xl', Styles.text.title)}>{MESSAGES.HEADING}</h1>
                    <p className={Styles.text.subtitle}>{MESSAGES.SUBTITLE}</p>
                </div>

                <Link to={`${ATTENDEES_ROUTE}/add`} className="w-full md:w-auto">
                    <Button
                        size="lg"
                        style={{ backgroundColor: Styles.colors.hubCyan }}
                        className={cn('w-full md:w-auto px-8 py-6 text-lg', Styles.actions.primaryButton)}
                    >
                        {MESSAGES.ADD_BUTTON}
                    </Button>
                </Link>
            </div>
        </Fragment>
    );

    const renderBody = () => {
        if (isLoading) {
            return (
                <Card className={cn('p-10 md:p-20 text-center border-dashed', Styles.glass.card)}>
                    <p className={cn('text-xl font-medium', Styles.text.subtitle)}>{MESSAGES.LOADING_STATE}</p>
                </Card>
            );
        }

        if (!data || data.length === 0) {
            return (
                <Card className={cn('p-10 md:p-20 text-center border-dashed', Styles.glass.card)}>
                    <p className={cn('text-xl font-medium', Styles.text.subtitle)}>{MESSAGES.EMPTY_STATE}</p>
                </Card>
            );
        }

        return (
            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                {data.map((attendee) => (
                    <Card
                        key={attendee.id}
                        className={cn('p-6 rounded-2xl flex flex-col gap-5', Styles.glass.card, Styles.glass.cardHover)}
                    >
                        <div className="min-w-0">
                            <h2 className="text-xl font-semibold text-white truncate">{attendee.name}</h2>
                            <p className="text-blue-200/70 break-all">{attendee.email}</p>
                        </div>

                        <div className="flex flex-wrap gap-2">
                            <Badge variant="outline" className="border-white/20 text-white">
                                {MESSAGES.TICKET_TYPE_LABELS[attendee.ticket_type] ?? attendee.ticket_type}
                            </Badge>
                            <Badge
                                variant="outline"
                                className={
                                    attendee.has_paid
                                        ? 'border-green-400/40 text-green-300'
                                        : 'border-red-400/40 text-red-300'
                                }
                            >
                                {attendee.has_paid ? MESSAGES.PAID : MESSAGES.NOT_PAID}
                            </Badge>
                        </div>

                        <div className="flex flex-col sm:flex-row gap-3 mt-auto">
                            <Link to={`${ATTENDEES_ROUTE}/${attendee.id}`} className="flex-1">
                                <Button
                                    variant="outline"
                                    className="w-full bg-white/5 border-white/10 text-white hover:bg-white/20 hover:text-white transition-all"
                                >
                                    {MESSAGES.EDIT_BUTTON}
                                </Button>
                            </Link>

                            <Button
                                style={{ backgroundColor: Styles.colors.hubCyan }}
                                className="flex-1 text-white font-semibold hover:opacity-90 transition-all"
                                disabled={isSendingTicketFor(attendee.id)}
                                onClick={() => handleSendTicket(attendee)}
                            >
                                {isSendingTicketFor(attendee.id)
                                    ? MESSAGES.SENDING_TICKET_BUTTON
                                    : MESSAGES.SEND_TICKET_BUTTON}
                            </Button>

                            <Button
                                variant="destructive"
                                className="flex-1 shadow-lg shadow-red-500/10 hover:shadow-red-500/20 transition-all"
                                disabled={deleteMutation.isPending && deleteMutation.variables === attendee.id}
                                onClick={() => handleDelete(attendee)}
                            >
                                {MESSAGES.DELETE_BUTTON}
                            </Button>
                        </div>
                    </Card>
                ))}
            </div>
        );
    };

    return (
        <Fragment>
            <Helmet>
                <title>{MESSAGES.PAGE_TITLE}</title>
            </Helmet>

            <div className={cn('min-h-screen p-4 sm:p-8', Styles.backgrounds.primaryGradient)}>
                <div className="max-w-7xl mx-auto">
                    {header}
                    {renderBody()}
                </div>
            </div>
        </Fragment>
    );
}
