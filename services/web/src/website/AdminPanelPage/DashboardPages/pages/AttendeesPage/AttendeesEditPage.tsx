import { Button } from '@/components/ui/button.tsx';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card.tsx';
import { Form } from '@/components/ui/form.tsx';
import { cn } from '@/lib/utils.ts';
import { apiClient } from '@/services/apiClient.ts';
import type { Attendee } from '@/types/attendee.ts';
import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Fragment, useEffect } from 'react';
import { Helmet } from 'react-helmet';
import { useForm } from 'react-hook-form';
import { useNavigate, useParams } from 'react-router';
import { Styles } from '../../../AdminStyle.ts';
import { AttendeeFormFields } from './components/AttendeeFormFields.tsx';
import { ATTENDEES_ENDPOINT, ATTENDEES_QUERY_KEY, ATTENDEES_ROUTE, unwrapAttendee } from './constants.ts';
import { AttendeesAddMessages, AttendeesEditMessages } from './messages.tsx';
import { type AttendeeFormData, attendeeSchema } from './validation/validation.tsx';

export function AttendeesEditPage() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const queryClient = useQueryClient();
    const isEditMode = Boolean(id);
    const MESSAGES = isEditMode ? AttendeesEditMessages : AttendeesAddMessages;

    const form = useForm<AttendeeFormData>({
        resolver: zodResolver(attendeeSchema),
        defaultValues: {
            name: '',
            email: '',
            ticket_type: undefined,
            has_paid: false,
        },
        mode: 'onTouched',
    });

    const { control, handleSubmit, reset } = form;

    // Fetch the attendee when editing
    const { data: attendee, isLoading } = useQuery({
        queryKey: [ATTENDEES_QUERY_KEY, id],
        queryFn: () => apiClient.get<{ attendee: Attendee } | Attendee>(`${ATTENDEES_ENDPOINT}/${id}`),
        enabled: isEditMode,
        select: unwrapAttendee,
    });

    // Prefill the form when editing
    useEffect(() => {
        if (attendee) {
            reset({
                name: attendee.name,
                email: attendee.email,
                ticket_type: attendee.ticket_type,
                has_paid: attendee.has_paid,
            });
        }
    }, [attendee, reset]);

    const mutation = useMutation({
        mutationFn: (data: AttendeeFormData) =>
            isEditMode
                ? apiClient.patch<Attendee, AttendeeFormData>(`${ATTENDEES_ENDPOINT}/${id}`, data)
                : apiClient.post<Attendee, AttendeeFormData>(`${ATTENDEES_ENDPOINT}/`, data),
        onSuccess: async () => {
            await queryClient.invalidateQueries({ queryKey: [ATTENDEES_QUERY_KEY] });
            navigate(ATTENDEES_ROUTE);
        },
        onError: (error) => alert(error.message),
    });

    const onSubmit = (data: AttendeeFormData) => mutation.mutate(data);

    const goBack = () => navigate(ATTENDEES_ROUTE);

    const pageWrapperClass = cn('min-h-screen p-4 sm:p-8', Styles.backgrounds.primaryGradient);

    if (isEditMode && isLoading) {
        return (
            <div className={pageWrapperClass}>
                <div className="max-w-3xl mx-auto text-white text-center py-20">
                    {AttendeesEditMessages.LOADING_STATE}
                </div>
            </div>
        );
    }

    if (isEditMode && !attendee) {
        return (
            <Fragment>
                <Helmet>
                    <title>{AttendeesEditMessages.NOT_FOUND_TITLE}</title>
                </Helmet>
                <div className={pageWrapperClass}>
                    <div className="max-w-2xl mx-auto">
                        <Card className={cn('p-12 text-center', Styles.glass.card)}>
                            <p className="text-red-400 text-lg mb-6">{AttendeesEditMessages.NOT_FOUND_MESSAGE}</p>
                            <Button
                                style={{ backgroundColor: Styles.colors.hubCyan }}
                                className="text-white hover:opacity-90 transition-opacity"
                                onClick={goBack}
                            >
                                {AttendeesEditMessages.RETURN_BUTTON}
                            </Button>
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

            <div className={pageWrapperClass}>
                <div className="max-w-3xl mx-auto">
                    <Button variant="ghost" onClick={goBack} className={cn('mb-4', Styles.glass.ghostButton)}>
                        {MESSAGES.BACK_BUTTON}
                    </Button>

                    <Card className={Styles.glass.card}>
                        <CardHeader className="border-b border-white/5 pb-8">
                            <CardTitle className={cn('text-2xl md:text-3xl', Styles.text.title)}>
                                {MESSAGES.HEADING}
                            </CardTitle>
                            <p className={Styles.text.subtitle}>{MESSAGES.SUBTITLE}</p>
                        </CardHeader>

                        <Form {...form}>
                            <form onSubmit={handleSubmit(onSubmit)}>
                                <CardContent className="p-6 md:p-8">
                                    <div className={Styles.forms.fieldContainer}>
                                        <div className="form-dark-theme">
                                            <AttendeeFormFields control={control} />
                                        </div>
                                    </div>
                                </CardContent>

                                <CardFooter
                                    className={cn(
                                        'flex flex-col sm:flex-row gap-4 p-6 md:p-8',
                                        Styles.backgrounds.footerDark,
                                    )}
                                >
                                    <Button
                                        type="button"
                                        variant="outline"
                                        className={cn('w-full sm:flex-1', Styles.actions.secondaryButton)}
                                        onClick={goBack}
                                    >
                                        {MESSAGES.CANCEL_BUTTON}
                                    </Button>
                                    <Button
                                        type="submit"
                                        disabled={mutation.isPending}
                                        style={{ backgroundColor: Styles.colors.hubCyan }}
                                        className="w-full sm:flex-1 text-white font-bold shadow-lg shadow-blue-500/20 transition-all hover:opacity-90"
                                    >
                                        {mutation.isPending ? MESSAGES.SUBMITTING_BUTTON : MESSAGES.SUBMIT_BUTTON}
                                    </Button>
                                </CardFooter>
                            </form>
                        </Form>
                    </Card>
                </div>
            </div>
        </Fragment>
    );
}
