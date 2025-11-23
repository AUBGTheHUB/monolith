import { Fragment } from 'react/jsx-runtime';
import { useNavigate } from 'react-router';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Helmet } from 'react-helmet';
import { useJudgeForm } from './hooks/useJudgeForm';
import { JudgeFormFields } from './components/JudgeFormFields';

export function JudgesAddPage() {
    const navigate = useNavigate();
    const { formData, errors, handleChange, validate } = useJudgeForm();

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (!validate()) return;

        console.log('Creating judge:', formData);
        alert('Judge added successfully!');

        // TODO: Replace with API call
        // await createJudge(formData);
        // navigate('/dashboard/judges');
    };

    return (
        <Fragment>
            <Helmet>
                <title>Add Judge - Admin Dashboard</title>
            </Helmet>

            <div className="min-h-screen bg-gray-50 p-8">
                <div className="max-w-2xl mx-auto">
                    <Button variant="ghost" onClick={() => navigate('/dashboard/judges')} className="mb-4">
                        ← Back to Judges
                    </Button>

                    <Card>
                        <CardHeader>
                            <CardTitle className="text-3xl">Add New Judge</CardTitle>
                            <p className="text-gray-600 mt-2">Fill in the details to add a new judge</p>
                        </CardHeader>

                        <form onSubmit={handleSubmit}>
                            <CardContent className="space-y-6">
                                <JudgeFormFields formData={formData} errors={errors} onChange={handleChange} />
                            </CardContent>

                            <CardFooter className="flex gap-3">
                                <Button
                                    type="button"
                                    variant="outline"
                                    className="flex-1"
                                    onClick={() => navigate('/dashboard/judges')}
                                >
                                    Cancel
                                </Button>
                                <Button type="submit" className="flex-1 bg-blue-600 hover:bg-blue-700">
                                    Add Judge
                                </Button>
                            </CardFooter>
                        </form>
                    </Card>
                </div>
            </div>
        </Fragment>
    );
}
