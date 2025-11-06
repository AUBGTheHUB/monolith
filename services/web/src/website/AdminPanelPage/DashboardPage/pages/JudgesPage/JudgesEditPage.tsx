import { Fragment } from 'react/jsx-runtime';
import { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router';
import { MOCK_JUDGES } from '@/lib/judges.mock';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Helmet } from 'react-helmet';
import { useJudgeForm } from './hooks/useJudgeForm';
import { JudgeFormFields } from './components/JudgeFormFields';

// Text constants for Edit page
const MESSAGES = {
    PAGE_TITLE: 'Edit Judge - Admin Dashboard',
    NOT_FOUND_TITLE: 'Judge Not Found - Admin Dashboard',
    HEADING: 'Edit Judge',
    SUBTITLE: 'Update judge information',
    BACK_BUTTON: '← Back to Judges',
    NOT_FOUND_MESSAGE: 'Judge not found',
    RETURN_BUTTON: 'Return to Judges List',
    CANCEL_BUTTON: 'Cancel',
    SUBMIT_BUTTON: 'Update Judge',
    SUCCESS_MESSAGE: 'Judge updated successfully! (This is a mock - no API call made)',
};

export function JudgesEditPage() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();

    const judge = MOCK_JUDGES.find((j) => j.id === id);

    const { formData, errors, handleChange, validate, setFormData } = useJudgeForm();

    useEffect(() => {
        if (judge) {
            setFormData({
                name: judge.name,
                companyName: judge.companyName,
                imageUrl: judge.imageUrl,
            });
        }
    }, [judge, setFormData]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (!validate()) {
            return; 
        }

        console.log('Updating judge:', { id, ...formData });

        // TODO: Replace with actual API call
        // Example:
        // try {
        //     await updateJudge(id, formData);
        //     navigate('/dashboard/judges');
        // } catch (error) {
        //     console.error('Failed to update judge:', error);
        // }

        alert(MESSAGES.SUCCESS_MESSAGE);
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

                        <form onSubmit={handleSubmit}>
                            <CardContent className="space-y-6">
                                {/* All three form fields (Name, Company, Image) */}
                                <JudgeFormFields formData={formData} errors={errors} onChange={handleChange} />
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
                    </Card>
                </div>
            </div>
        </Fragment>
    );
}
