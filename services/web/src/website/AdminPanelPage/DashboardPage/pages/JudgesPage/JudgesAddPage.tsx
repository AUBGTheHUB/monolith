import { Fragment } from 'react/jsx-runtime';
import { useNavigate } from 'react-router';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Helmet } from 'react-helmet';
import { JudgeFormFields } from './components/JudgeFormFields';
import { Form } from '@/components/ui/form';
import { judgeSchema, JudgeFormData } from './validation/validation';

export function JudgesAddPage() {
    const navigate = useNavigate();

    const form = useForm<JudgeFormData>({
        resolver: zodResolver(judgeSchema),
        defaultValues: {
            name: '',
            companyName: '',
            imageUrl: '',
        },
        mode: 'onTouched',
    });

    const { control, handleSubmit, watch } = form;
    const imageUrl = watch('imageUrl');

    const onSubmit = (data: JudgeFormData) => {
        console.log('Creating judge:', data);
        alert('Judge added successfully!');
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

                        <Form {...form}>
                            <form onSubmit={handleSubmit(onSubmit)}>
                                <CardContent className="flex flex-col md:flex-row gap-8">
                                    <div className="flex-1 space-y-6">
                                        <JudgeFormFields control={control} />
                                    </div>
                                    <div className="flex-1 flex flex-col items-center justify-start gap-2">
                                        <span className="text-sm font-medium text-gray-500 self-start">Preview</span>
                                        {imageUrl ? (
                                            <div
                                                className="w-full max-w-[300px] aspect-square rounded-lg border 
                                                    border-gray-200 overflow-hidden bg-gray-50"
                                            >
                                                <img
                                                    src={imageUrl}
                                                    alt="Preview"
                                                    className="w-full h-full object-cover"
                                                    onError={(e) => {
                                                        (e.target as HTMLImageElement).src =
                                                            'https://placehold.co/300?text=Invalid+Image';
                                                    }}
                                                />
                                            </div>
                                        ) : (
                                            <div
                                                className="w-full max-w-[300px] aspect-square rounded-lg border-2 
                                                    border-dashed border-gray-200 flex items-center justify-center 
                                                    text-gray-400 bg-gray-50"
                                            >
                                                No image URL provided
                                            </div>
                                        )}
                                    </div>
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
                        </Form>
                    </Card>
                </div>
            </div>
        </Fragment>
    );
}
