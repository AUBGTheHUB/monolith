import { Fragment } from 'react/jsx-runtime';
import { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { MOCK_JUDGES } from '@/lib/judges.mock';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Helmet } from 'react-helmet';
import { JudgeFormFields } from './components/JudgeFormFields';
import { JudgesEditMessages as MESSAGES } from './messagesConsts';
import { Form } from '@/components/ui/form';
import { judgeSchema, JudgeFormData } from './lib/judges.validation';

export function JudgesEditPage() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();

    const judge = MOCK_JUDGES.find((j) => j.id === id);

    const form = useForm<JudgeFormData>({
        resolver: zodResolver(judgeSchema),
        defaultValues: {
            name: '',
            companyName: '',
            imageUrl: '',
        },
        mode: 'onTouched',
    });

    const { control, handleSubmit, reset } = form;

    useEffect(() => {
        if (judge) {
            reset({
                name: judge.name,
                companyName: judge.companyName,
                imageUrl: judge.imageUrl,
            });
        }
    }, [judge, reset]);

    const onSubmit = (data: JudgeFormData) => {
        console.log('Updating judge:', { id, ...data });
        alert(MESSAGES.SUCCESS_MESSAGE);
        // TODO: Replace with actual API call
        // try {
        //     await updateJudge(id, data);
        //     navigate('/dashboard/judges');
        // } catch (error) {
        //     console.error('Failed to update judge:', error);
        // }
    };

    const goBack = () => {
        navigate('/dashboard/judges');
    };

    if (!judge) {
        return (
            <Fragment>
                <Helmet>
                    <title>{MESSAGES.NOT_FOUND_TITLE}</title>
                </Helmet>
                <div className="min-h-screen bg-gray-50 p-8">
                    <div className="max-w-2xl mx-auto">
                        <Card className="p-12 text-center">
                            <p className="text-red-500 text-lg mb-4">{MESSAGES.NOT_FOUND_MESSAGE}</p>
                            <Button onClick={goBack}>{MESSAGES.RETURN_BUTTON}</Button>
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

            <div className="min-h-screen bg-gray-50 p-8">
                <div className="max-w-2xl mx-auto">
                    <Button variant="ghost" onClick={goBack} className="mb-4">
                        {MESSAGES.BACK_BUTTON}
                    </Button>

                    <Card>
                        <CardHeader>
                            <CardTitle className="text-3xl">{MESSAGES.HEADING}</CardTitle>
                            <p className="text-gray-600 mt-2">{MESSAGES.SUBTITLE}</p>
                        </CardHeader>

                        <Form {...form}>
                            <form onSubmit={handleSubmit(onSubmit)}>
                                <CardContent className="space-y-6">
                                    <JudgeFormFields control={control} />
                                </CardContent>

                                <CardFooter className="flex gap-3">
                                    <Button type="button" variant="outline" className="flex-1" onClick={goBack}>
                                        {MESSAGES.CANCEL_BUTTON}
                                    </Button>
                                    <Button type="submit" className="flex-1 bg-blue-600 hover:bg-blue-700">
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
