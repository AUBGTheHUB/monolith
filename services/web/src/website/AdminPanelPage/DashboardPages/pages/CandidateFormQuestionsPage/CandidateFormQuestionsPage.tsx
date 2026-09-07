import { Fragment, useEffect } from 'react';
import { Link } from 'react-router';
import { Card } from '@/components/ui/card.tsx';
import { Button } from '@/components/ui/button.tsx';
import { Helmet } from 'react-helmet';
import { CandidateFormQuestionMessages as MESSAGES } from './messages.tsx';
import { Styles } from '../../../AdminStyle.ts';
import { cn } from '@/lib/utils.ts';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { apiClient } from '@/services/apiClient.ts';
import { Question } from '@/types/question.ts';

export function CandidateFormQuestionsPage() {
    const queryClient = useQueryClient();
    // Fetch
    const { data, isLoading, error, isError } = useQuery({
        queryKey: ['questions'],
        queryFn: () => apiClient.get<{ questions: Question[] }>('/admin/candidate-form/questions'),
        select: (res) => res.questions,
    });
    useEffect(() => {
        if (isError) {
            console.error(error);
            alert(error);
        }
    });

    // fix urls
    const deleteMutation = useMutation({
        mutationFn: (id: string) => apiClient.delete(`/admin/questions/${id}`),
        onSuccess: async () => {
            await queryClient.invalidateQueries({ queryKey: ['questions'] });
        },
        onError: (error) => alert(error.message),
    });

    const handleDelete = (id: string, prompt: string) => {
        if (window.confirm(MESSAGES.DELETE_CONFIRM(prompt))) {
            deleteMutation.mutate(id);
        }
    };

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

                            <Link to="/admin/dashboard/candidate-form-questions/add">
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

                        <Link to="/admin/dashboard/candidate-form-questions/add">
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
                        <div className="grid grid-cols-1 gap-8">
                            {data.map((question) => (
                                <div key={question.id} className="group">
                                    <p>{question.prompt}</p>

                                    <div className="flex gap-3 w-full">
                                        <Link
                                            to={`/admin/dashboard/candidate-form-questions/${question.id}`}
                                            className="flex-1"
                                        >
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
                                            onClick={() => handleDelete(question.id, question.prompt)}
                                        >
                                            {MESSAGES.DELETE_BUTTON}
                                        </Button>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </div>
        </Fragment>
    );
}
