import { Fragment } from 'react/jsx-runtime';
import { useState } from 'react';
import { useNavigate } from 'react-router';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Helmet } from 'react-helmet';

export function JudgesAddPage() {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        name: '',
        companyName: '',
        imageUrl: '',
    });
    const [errors, setErrors] = useState({
        name: '',
        companyName: '',
        imageUrl: '',
    });

    const validateField = (field: string, value: string) => {
        let error = '';

        if (field === 'name') {
            if (!value.trim()) {
                error = 'Name is required';
            } else if (value.length < 2) {
                error = 'Name must be at least 2 characters';
            } else if (value.length > 100) {
                error = 'Name must be less than 100 characters';
            }
        }

        if (field === 'companyName') {
            if (!value.trim()) {
                error = 'Company name is required';
            } else if (value.length < 2) {
                error = 'Company name must be at least 2 characters';
            } else if (value.length > 100) {
                error = 'Company name must be less than 100 characters';
            }
        }

        if (field === 'imageUrl') {
            if (!value.trim()) {
                error = 'Image URL is required';
            }
        }

        return error;
    };

    const handleChange = (field: string, value: string) => {
        setFormData((prev) => ({ ...prev, [field]: value }));
        const error = validateField(field, value);
        setErrors((prev) => ({ ...prev, [field]: error }));
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        // Validate all fields
        const nameError = validateField('name', formData.name);
        const companyError = validateField('companyName', formData.companyName);
        const imageError = validateField('imageUrl', formData.imageUrl);

        setErrors({
            name: nameError,
            companyName: companyError,
            imageUrl: imageError,
        });

        // If no errors, submit (in real app, this would call API)
        if (!nameError && !companyError && !imageError) {
            console.log('Creating judge:', formData);
            // TODO: API call would go here
            // navigate('/dashboard/judges');
            alert('Judge added successfully! (This is a mock - no API call made)');
        }
    };

    return (
        <Fragment>
            <Helmet>
                <title>Add Judge - Admin Dashboard</title>
                <link rel="icon" href="/faviconHack.ico" />
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
                                <div className="space-y-2">
                                    <Label htmlFor="name" className="text-base">
                                        Name <span className="text-red-500">*</span>
                                    </Label>
                                    <Input
                                        id="name"
                                        placeholder="Enter judge's full name"
                                        value={formData.name}
                                        onChange={(e) => handleChange('name', e.target.value)}
                                        className={errors.name ? 'border-red-500' : ''}
                                    />
                                    {errors.name && <p className="text-sm text-red-500">{errors.name}</p>}
                                    <p className="text-xs text-gray-500">2-100 characters</p>
                                </div>

                                <div className="space-y-2">
                                    <Label htmlFor="companyName" className="text-base">
                                        Company Name <span className="text-red-500">*</span>
                                    </Label>
                                    <Input
                                        id="companyName"
                                        placeholder="Enter company name"
                                        value={formData.companyName}
                                        onChange={(e) => handleChange('companyName', e.target.value)}
                                        className={errors.companyName ? 'border-red-500' : ''}
                                    />
                                    {errors.companyName && <p className="text-sm text-red-500">{errors.companyName}</p>}
                                    <p className="text-xs text-gray-500">2-100 characters</p>
                                </div>

                                <div className="space-y-2">
                                    <Label htmlFor="imageUrl" className="text-base">
                                        Image URL <span className="text-red-500">*</span>
                                    </Label>
                                    <Input
                                        id="imageUrl"
                                        placeholder="Enter image URL (e.g., /judge_photo.webp)"
                                        value={formData.imageUrl}
                                        onChange={(e) => handleChange('imageUrl', e.target.value)}
                                        className={errors.imageUrl ? 'border-red-500' : ''}
                                    />
                                    {errors.imageUrl && <p className="text-sm text-red-500">{errors.imageUrl}</p>}
                                    {formData.imageUrl && (
                                        <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                                            <p className="text-sm text-gray-600 mb-2">Preview:</p>
                                            <img
                                                src={formData.imageUrl}
                                                alt="Preview"
                                                className="w-24 h-24 rounded-full object-cover"
                                                onError={(e) => {
                                                    e.currentTarget.src =
                                                        'https://via.placeholder.com/150?text=Invalid+URL';
                                                }}
                                            />
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
                    </Card>
                </div>
            </div>
        </Fragment>
    );
}
