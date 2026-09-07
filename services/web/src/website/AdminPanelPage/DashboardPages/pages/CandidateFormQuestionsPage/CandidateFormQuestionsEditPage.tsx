import { Fragment } from 'react/jsx-runtime';
import { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card.tsx';
import { Button } from '@/components/ui/button.tsx';
import { Helmet } from 'react-helmet';
import { CandidateFormQuestionsFormFields } from './components/CandidateFormQuestionFormFields.tsx';
import { CandidateFormQuestionAddMessages, CandidateFormQuestionEditMessages } from './messages.tsx';
import { Form } from '@/components/ui/form.tsx';
import { CandidateFormQuestionFormData, baseSchema } from './validation/validation.tsx';
import { Styles } from '../../../AdminStyle.ts';
import { cn } from '@/lib/utils.ts';
import { useQueryClient, useQuery, useMutation } from '@tanstack/react-query';
import { apiClient } from '@/services/apiClient.ts';
import { toFormData } from '@/helpers/formHelpers.ts';
import { Question } from '@/types/question.ts';

export function CandidateFormQuestionsEditPage() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const queryClient = useQueryClient();
    const isEditMode = Boolean(id);
    const MESSAGES = isEditMode ? CandidateFormQuestionEditMessages : CandidateFormQuestionAddMessages;
    const form = useForm<CandidateFormQuestionFormData>({
        resolver: zodResolver(baseSchema),
        defaultValues: {
            prompt: '',
            // fix
            question_type: [],
            answer_type: [],
            options: '',
        },
        mode: 'onTouched',
    });

    const { control, handleSubmit, reset } = form;

    // Fetch if in Edit mode
    const { data: question, isLoading } = useQuery({
        queryKey: ['question', id],
        queryFn: () => apiClient.get<{ question: Question }>(`/admin/question/${id}`),
        enabled: isEditMode,
        select: (res) => res.question,
    });

    // Load defaults in edit
    useEffect(() => {
        if (question) {
            reset({
                prompt: question.prompt,
                answer_type: question.answer_type,
                question_type: question.question_type,
                options: question.options,
            });
        }
    }, [question, reset]);

    const mutation = useMutation({
        mutationFn: (formData: FormData) => {
            return isEditMode
                ? apiClient.patchForm<Question>(`/admin/questions/${id}`, formData)
                : apiClient.postForm<Question>('/admin/questions', formData);
        },
        onSuccess: async () => {
            await queryClient.invalidateQueries({ queryKey: ['questions'] });
            navigate('/admin/dashboard/candidate-form-questions');
        },
        onError: (error) => {
            alert(error.message);
        },
    });
    const onSubmit = (data: CandidateFormQuestionFormData) => {
        // Wrap data as FormData object using our custom helper
        const formData = toFormData(data);
        mutation.mutate(formData);
    };

    const goBack = () => {
        navigate('/admin/dashboard/candidate-form-questions');
    };

    const pageWrapperClass = cn('min-h-screen p-8', Styles.backgrounds.primaryGradient);
    if (isEditMode && isLoading) {
        return (
            <div className={pageWrapperClass}>
                <div className="max-w-5xl mx-auto text-white text-center py-20">
                    {CandidateFormQuestionEditMessages.LOADING_STATE}
                </div>
            </div>
        );
    }
    if (isEditMode && !question) {
        return (
            <Fragment>
                <Helmet>
                    <title>{CandidateFormQuestionEditMessages.NOT_FOUND_TITLE}</title>
                </Helmet>
                <div className={pageWrapperClass}>
                    <div className="max-w-2xl mx-auto">
                        <Card className={cn('p-12 text-center', Styles.glass.card)}>
                            <p className="text-red-400 text-lg mb-6">
                                {CandidateFormQuestionEditMessages.NOT_FOUND_MESSAGE}
                            </p>
                            <Button
                                style={{ backgroundColor: Styles.colors.hubCyan }}
                                className="text-white hover:opacity-90 transition-opacity"
                                onClick={goBack}
                            >
                                {CandidateFormQuestionEditMessages.RETURN_BUTTON}
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
                                            <CandidateFormQuestionsFormFields control={control} />
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
