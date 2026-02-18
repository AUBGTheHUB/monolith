import { Fragment } from 'react/jsx-runtime';
import { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card.tsx';
import { Button } from '@/components/ui/button.tsx';
import { Helmet } from 'react-helmet';
import { JudgeFormFields } from './components/JudgeFormFields.tsx';
import { JudgesEditMessages, JudgesAddMessages } from './messages.tsx';
import { Judge } from '@/types/judge.ts';
import { Form } from '@/components/ui/form.tsx';
import { judgeSchema, JudgeFormData } from './validation/validation.tsx';
import { Styles } from '../../../AdminStyle.ts';
import { cn } from '@/lib/utils.ts';
import { useQueryClient, useQuery, useMutation } from '@tanstack/react-query';
import { apiClient } from '@/services/apiClient.ts';

export function JudgesEditPage() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const queryClient = useQueryClient();
    const isEditMode = Boolean(id);
    const MESSAGES = isEditMode ? JudgesEditMessages : JudgesAddMessages;

    const form = useForm<JudgeFormData>({
        resolver: zodResolver(judgeSchema),
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
    const { data: judge, isLoading } = useQuery({
        queryKey: ['judge', id],
        queryFn: () => apiClient.get<{ judge: Judge }>(`/admin/judges/${id}`),
        enabled: isEditMode,
        select: (res) => res.judge,
    });
    // Load defaults in edit
    useEffect(() => {
        if (judge) {
            reset({
                name: judge.name,
                company: judge.company,
                avatar_url: judge.avatar_url,
                job_title: judge.job_title || '',
                linkedin_url: judge.linkedin_url || '',
            });
        }
    }, [judge, reset]);

    const mutation = useMutation({
        mutationFn: (formData: JudgeFormData) => {
            return isEditMode
                ? apiClient.patch<Judge, JudgeFormData>(`/admin/judges/${id}`, formData)
                : apiClient.post<Judge, JudgeFormData>('/admin/judges', formData);
        },
        onSuccess: async () => {
            await queryClient.invalidateQueries({ queryKey: ['judges'] });
            navigate('/admin/dashboard/judges');
        },
        onError: (error) => {
            alert(error.message);
        },
    });
    const onSubmit = (data: JudgeFormData) => {
        mutation.mutate(data);
    };

    const goBack = () => {
        navigate('/admin/dashboard/judges');
    };

    const pageWrapperClass = cn('min-h-screen p-8', Styles.backgrounds.primaryGradient);
    if (isEditMode && isLoading) {
        return (
            <div className={pageWrapperClass}>
                <div className="max-w-5xl mx-auto text-white text-center py-20">{JudgesEditMessages.LOADING_STATE}</div>
            </div>
        );
    }
    if (isEditMode && !judge) {
        return (
            <Fragment>
                <Helmet>
                    <title>{JudgesEditMessages.NOT_FOUND_TITLE}</title>
                </Helmet>
                <div className={pageWrapperClass}>
                    <div className="max-w-2xl mx-auto">
                        <Card className={cn('p-12 text-center', Styles.glass.card)}>
                            <p className="text-red-400 text-lg mb-6">{JudgesEditMessages.NOT_FOUND_MESSAGE}</p>
                            <Button
                                style={{ backgroundColor: Styles.colors.hubCyan }}
                                className="text-white hover:opacity-90 transition-opacity"
                                onClick={goBack}
                            >
                                {JudgesEditMessages.RETURN_BUTTON}
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
                                            <JudgeFormFields control={control} />
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
