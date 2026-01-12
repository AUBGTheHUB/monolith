import { Fragment } from 'react/jsx-runtime';
import { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { MOCK_JUDGES } from '@/website/AdminPanelPage/DashboardPage/pages/JudgesPage/mockJudges';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Helmet } from 'react-helmet';
import { JudgeFormFields } from './components/JudgeFormFields';
import { JudgesEditMessages as MESSAGES } from './messages';
import { Form } from '@/components/ui/form';
import { judgeSchema, JudgeFormData } from './validation/validation';
import { Styles } from '../../../AdminStyle';
import { cn } from '@/utils';

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
            position: '',
            linkedinURL: '',
        },
        mode: 'onTouched',
    });

    const { control, handleSubmit, reset, watch } = form;
    const imageUrl = watch('imageUrl');

    useEffect(() => {
        if (judge) {
            reset({
                name: judge.name,
                companyName: judge.companyName,
                imageUrl: judge.imageUrl,
                position: judge.position || '',
                linkedinURL: judge.linkedinURL || '',
            });
        }
    }, [judge, reset]);

    const onSubmit = () => {
        alert(MESSAGES.SUCCESS_MESSAGE);
    };

    const goBack = () => {
        navigate('/admin/dashboard/judges');
    };

    const pageWrapperClass = cn('min-h-screen p-8', Styles.backgrounds.primaryGradient);

    if (!judge) {
        return (
            <Fragment>
                <Helmet>
                    <title>{MESSAGES.NOT_FOUND_TITLE}</title>
                </Helmet>
                <div className={pageWrapperClass}>
                    <div className="max-w-2xl mx-auto">
                        <Card className={cn('p-12 text-center', Styles.glass.card)}>
                            <p className="text-red-400 text-lg mb-6">{MESSAGES.NOT_FOUND_MESSAGE}</p>
                            <Button
                                style={{ backgroundColor: Styles.colors.hubCyan }}
                                className="text-white hover:opacity-90 transition-opacity"
                                onClick={goBack}
                            >
                                {MESSAGES.RETURN_BUTTON}
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
                                        className={Styles.forms.fieldContainer}
                                        onClick={goBack}
                                    >
                                        {MESSAGES.CANCEL_BUTTON}
                                    </Button>
                                    <Button
                                        type="submit"
                                        style={{ backgroundColor: Styles.colors.hubCyan }}
                                        className={Styles.forms.fieldContainer}
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
