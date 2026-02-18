import { Button } from '@/components/ui/button.tsx';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card.tsx';
import { Form } from '@/components/ui/form.tsx';
import { cn } from '@/lib/utils.ts';
import { apiClient } from '@/services/apiClient.ts';
import { Mentor } from '@/types/mentor.ts';
import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useEffect } from 'react';
import { Helmet } from 'react-helmet';
import { useForm } from 'react-hook-form';
import { useNavigate, useParams } from 'react-router';
import { Fragment } from 'react/jsx-runtime';
import { Styles } from '../../../AdminStyle.ts';
import { MentorFormFields } from './components/MentorFormFields.tsx';
import { MentorsAddMessages, MentorsEditMessages } from './messages.tsx';
import { mentorSchema, type MentorFormData } from './validation';

export function MentorsEditPage() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const queryClient = useQueryClient();
    const isEditMode = Boolean(id);
    const MESSAGES = isEditMode ? MentorsEditMessages : MentorsAddMessages;

    const form = useForm<MentorFormData>({
        resolver: zodResolver(mentorSchema),
        defaultValues: {
            name: '',
            company: '',
            avatar_url: '',
            job_title: '',
            linkedin_url: '',
        },
        mode: 'onTouched',
    });

    const { control, handleSubmit, reset, watch } = form;
    const imageUrl = watch('avatar_url');

    // Fetch if in Edit mode
    const { data: mentor, isLoading } = useQuery({
        queryKey: ['mentor', id],
        queryFn: () => apiClient.get<{ mentor: Mentor }>(`/admin/mentors/${id}`),
        enabled: isEditMode,
        select: (res) => res.mentor,
    });

    // Load defaults in edit
    useEffect(() => {
        if (mentor) {
            reset({
                name: mentor.name,
                company: mentor.company,
                avatar_url: mentor.avatar_url,
                job_title: mentor.job_title || '',
                linkedin_url: mentor.linkedin_url || '',
            });
        }
    }, [mentor, reset]);

    const mutation = useMutation({
        mutationFn: (formData: MentorFormData) => {
            return isEditMode
                ? apiClient.patch<Mentor, MentorFormData>(`/admin/mentors/${id}`, formData)
                : apiClient.post<Mentor, MentorFormData>('/admin/mentors', formData);
        },
        onSuccess: async () => {
            await queryClient.invalidateQueries({ queryKey: ['mentors'] });
            navigate('/admin/dashboard/mentors');
        },
        onError: (error) => {
            alert(error.message);
        },
    });
    const onSubmit = (data: MentorFormData) => {
        mutation.mutate(data);
    };

    const goBack = () => {
        navigate('/admin/dashboard/mentors');
    };

    const pageWrapperClass = cn('min-h-screen p-8', Styles.backgrounds.primaryGradient);
    if (isEditMode && isLoading) {
        return (
            <div className={pageWrapperClass}>
                <div className="max-w-5xl mx-auto text-white text-center py-20">
                    {MentorsEditMessages.LOADING_STATE}
                </div>
            </div>
        );
    }
    if (isEditMode && !mentor) {
        return (
            <Fragment>
                <Helmet>
                    <title>{MentorsEditMessages.NOT_FOUND_TITLE}</title>
                </Helmet>
                <div className={pageWrapperClass}>
                    <div className="max-w-2xl mx-auto">
                        <Card className={cn('p-12 text-center', Styles.glass.card)}>
                            <p className="text-red-400 text-lg mb-6">{MentorsEditMessages.NOT_FOUND_MESSAGE}</p>
                            <Button
                                style={{ backgroundColor: Styles.colors.hubCyan }}
                                className="text-white hover:opacity-90 transition-opacity"
                                onClick={goBack}
                            >
                                {MentorsEditMessages.RETURN_BUTTON}
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
                                    <div className={Styles.forms.fieldContainer}>
                                        <div className="form-dark-theme">
                                            <MentorFormFields control={control} />
                                        </div>
                                    </div>

                                    <div className="flex-1 flex flex-col items-center justify-start gap-4">
                                        <span className={cn('self-start !text-white', Styles.text.label)}>Preview</span>

                                        <div
                                            className={cn(
                                                'relative w-full max-w-[500px] aspect-square rounded-lg flex items-center justify-center overflow-hidden',
                                                Styles.backgrounds.previewBox,
                                            )}
                                        >
                                            {imageUrl ? (
                                                <img
                                                    src={imageUrl}
                                                    alt="Preview"
                                                    className="w-full h-full object-cover"
                                                    onError={(e) => {
                                                        (e.target as HTMLImageElement).src =
                                                            'https://placehold.co/300?text=Invalid+Image';
                                                    }}
                                                />
                                            ) : (
                                                <p className={cn('px-4 text-center', Styles.colors.textMuted)}>
                                                    No image URL provided
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
}
