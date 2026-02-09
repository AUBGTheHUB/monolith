'use client';
import { Fragment, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { PastEvent } from '@/types/past-events';
import { Button } from '@/components/ui/button';
import { Helmet } from 'react-helmet';
import { PastEventFields } from './components/PastEventFormFields';
import { Form } from '@/components/ui/form';
import { PastEventsEditMessages, PastEventsAddMessages } from './messages';
import { pastEventSchema, PastEventFormData } from './validation/validation';
import { Styles } from '../../../AdminStyle';
import { cn } from '@/lib/utils';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/services/apiClient';

export const PastEventsEditPage = () => {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const queryClient = useQueryClient();
    const isEditMode = Boolean(id);
    const MESSAGES = isEditMode ? PastEventsEditMessages : PastEventsAddMessages;

    const form = useForm<PastEventFormData>({
        resolver: zodResolver(pastEventSchema),
        defaultValues: {
            title: '',
            cover_picture: '',
            tags: [],
        },
        mode: 'onTouched',
    });

    const { control, handleSubmit, reset, watch } = form;
    const imageValue = watch('cover_picture');

    // Fetch if in Edit mode
    const { data: event, isLoading } = useQuery({
        queryKey: ['event', id],
        queryFn: () => apiClient.get<{ past_event: PastEvent }>(`/admin/events/${id}`),
        enabled: isEditMode, // Only run if id exists
        select: (res) => res.past_event,
    });
    // Load default values in edit mode
    useEffect(() => {
        if (event) {
            reset({
                title: event.title,
                cover_picture: event.cover_picture,
                tags: event.tags || [],
            });
        }
    }, [event, reset]);

    // Mutation for save
    const mutation = useMutation({
        mutationFn: (formData: PastEventFormData) => {
            return isEditMode
                ? apiClient.patch<PastEvent, PastEventFormData>(`/admin/events/${id}`, formData)
                : apiClient.post<PastEvent, PastEventFormData>(`/admin/events`, formData);
        },
        onSuccess: async () => {
            await queryClient.invalidateQueries({ queryKey: ['events'] });
            navigate('/admin/dashboard/past-events');
        },
        onError: (error) => {
            alert(error.message);
        },
    });

    const onSubmit = (data: PastEventFormData) => {
        mutation.mutate(data);
    };

    const goBack = () => navigate('/admin/dashboard/past-events');

    const pageWrapperClass = cn('min-h-screen p-8', Styles.backgrounds.primaryGradient);
    if (isEditMode && isLoading) {
        return (
            <div className={pageWrapperClass}>
                <div className="max-w-5xl mx-auto text-white text-center py-20">
                    {PastEventsEditMessages.LOADING_STATE}
                </div>
            </div>
        );
    }

    if (isEditMode && !event) {
        return (
            <Fragment>
                <Helmet>
                    <title>{PastEventsEditMessages.NOT_FOUND_TITLE}</title>
                </Helmet>
                <div className={pageWrapperClass}>
                    <div className="max-w-2xl mx-auto">
                        <Card className={cn('p-12 text-center', Styles.glass.card)}>
                            <p className="text-red-400 text-lg mb-6">{PastEventsEditMessages.NOT_FOUND_MESSAGE}</p>
                            <Button
                                style={{ backgroundColor: Styles.colors.hubCyan }}
                                className="text-white hover:opacity-90 transition-opacity"
                                onClick={goBack}
                            >
                                {PastEventsEditMessages.RETURN_BUTTON}
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
                <div className="max-w-5xl mx-auto">
                    <Button variant="ghost" onClick={goBack} className={cn('mb-4', Styles.glass.ghostButton)}>
                        {MESSAGES.BACK_BUTTON}
                    </Button>

                    <Card className={Styles.glass.card}>
                        <CardHeader className="border-b border-white/5 pb-8">
                            <CardTitle className={cn('text-3xl', Styles.text.title)}>{MESSAGES.HEADING}</CardTitle>
                            <p className={Styles.text.subtitle}>{MESSAGES.SUBTITLE}</p>
                        </CardHeader>

                        <Form {...form}>
                            <form onSubmit={handleSubmit(onSubmit)}>
                                <CardContent className="flex flex-col md:flex-row gap-12 p-8">
                                    {/* Form fields */}
                                    <div className={Styles.forms.fieldContainer}>
                                        <div className="form-dark-theme">
                                            <PastEventFields control={control} />
                                        </div>
                                    </div>

                                    {/* Preview */}
                                    <div className="flex-1 flex flex-col items-center justify-start gap-4">
                                        <span className={cn('self-start !text-white', Styles.text.label)}>Preview</span>
                                        <div
                                            className={cn(
                                                'relative w-full max-w-[500px] aspect-square rounded-lg flex items-center justify-center overflow-hidden',
                                                Styles.backgrounds.previewBox,
                                            )}
                                        >
                                            {imageValue ? (
                                                <img
                                                    src={imageValue}
                                                    alt="Preview"
                                                    className="w-full h-full object-contain"
                                                    onError={(e) => {
                                                        (e.target as HTMLImageElement).src =
                                                            'https://placehold.co/300?text=Invalid+Image';
                                                    }}
                                                />
                                            ) : (
                                                <p className={cn('px-4 text-center', Styles.colors.textMuted)}>
                                                    No image provided
                                                </p>
                                            )}
                                        </div>
                                    </div>
                                </CardContent>

                                <CardFooter className={cn('flex gap-4 p-8', Styles.backgrounds.footerDark)}>
                                    <Button
                                        type="button"
                                        variant="outline"
                                        className="flex-1 text-black bg-white border-white hover:bg-gray-200 transition-colors"
                                        onClick={goBack}
                                    >
                                        {MESSAGES.CANCEL_BUTTON}
                                    </Button>
                                    <Button
                                        type="submit"
                                        style={{ backgroundColor: Styles.colors.hubCyan }}
                                        className="flex-1 text-white font-bold shadow-lg shadow-blue-500/20 transition-all hover:opacity-90"
                                    >
                                        {MESSAGES.SUBMIT_BUTTON}
                                    </Button>
                                </CardFooter>
                            </form>
                        </Form>
                    </Card>
                </div>
            </div>
        </Fragment>
    );
};
