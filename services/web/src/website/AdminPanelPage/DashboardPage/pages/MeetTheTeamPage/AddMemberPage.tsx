import { Fragment, useState, useRef } from 'react';
import { useNavigate, Link } from 'react-router';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { MultiSelect } from '@/components/ui/multi-select';
import { Helmet } from 'react-helmet';
import { toast } from 'react-toastify';
import { AVAILABLE_DEPARTMENTS, DEFAULT_PLACEHOLDER } from './constants';

export function AddMemberPage() {
    const navigate = useNavigate();
    const fileInputRef = useRef<HTMLInputElement>(null);

    const [formData, setFormData] = useState({
        name: '',
        image: DEFAULT_PLACEHOLDER,
    });
    const [imagePreview, setImagePreview] = useState<string>(DEFAULT_PLACEHOLDER);
    const [departments, setDepartments] = useState<string[]>([]);
    const [errors, setErrors] = useState<Record<string, string>>({});

    const handleImageClick = () => {
        fileInputRef.current?.click();
    };

    const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            if (!file.type.startsWith('image/')) {
                toast.error('Please upload an image file');
                return;
            }

            if (file.size > 5 * 1024 * 1024) {
                toast.error('Image size should be less than 5MB');
                return;
            }

            const reader = new FileReader();
            reader.onloadend = () => {
                const imageUrl = reader.result as string;
                setImagePreview(imageUrl);

                toast.success('Image uploaded successfully!');
            };
            reader.readAsDataURL(file);
        }
    };

    const validate = () => {
        const newErrors: Record<string, string> = {};

        if (!formData.name.trim()) {
            newErrors.name = 'Name is required';
        } else if (formData.name.length < 2) {
            newErrors.name = 'Name must be at least 2 characters';
        } else if (formData.name.length > 50) {
            newErrors.name = 'Name must be less than 50 characters';
        }

        if (departments.length === 0) {
            newErrors.departments = 'At least one department is required';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();

        if (!validate()) {
            return;
        }

        console.log('Creating team member:', { ...formData, departments });

        toast.success('Team member created successfully!');
        navigate('/dashboard/meet-the-team');
    };

    return (
        <Fragment>
            <Helmet>
                <title>Add Team Member - Admin Panel</title>
                <link rel="icon" href="/faviconHack.ico" />
            </Helmet>
            <div className="min-h-screen bg-gray-50 p-8">
                <div className="max-w-4xl mx-auto">
                    <Link to="/dashboard/meet-the-team">
                        <Button variant="ghost" className="mb-6">
                            ← Back to Team
                        </Button>
                    </Link>

                    <Card>
                        <CardHeader>
                            <CardTitle className="text-3xl">Add Team Member</CardTitle>
                            <p className="text-gray-600 mt-2">Create a new team member profile</p>
                        </CardHeader>
                        <CardContent>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                <div className="md:col-span-2">
                                    <form onSubmit={handleSubmit} className="space-y-6">
                                        <div>
                                            <Label htmlFor="name">Name *</Label>
                                            <Input
                                                id="name"
                                                placeholder="Enter team member name"
                                                value={formData.name}
                                                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                                className="mt-1"
                                            />
                                            {errors.name && <p className="text-red-500 text-sm mt-1">{errors.name}</p>}
                                        </div>

                                        <div>
                                            <Label>Departments *</Label>
                                            <div className="mt-2">
                                                <MultiSelect
                                                    options={AVAILABLE_DEPARTMENTS}
                                                    selected={departments}
                                                    onChange={setDepartments}
                                                    placeholder="Select departments..."
                                                />
                                            </div>
                                            {errors.departments && (
                                                <p className="text-red-500 text-sm mt-1">{errors.departments}</p>
                                            )}
                                        </div>

                                        <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700">
                                            Create Member
                                        </Button>
                                    </form>
                                </div>

                                <div className="md:col-span-1">
                                    <Label className="mb-2 block">Profile Picture</Label>
                                    <div
                                        className="relative w-full aspect-square rounded-lg overflow-hidden cursor-pointer group border-2 border-gray-200"
                                        onClick={handleImageClick}
                                    >
                                        <img
                                            src={imagePreview}
                                            alt="Profile preview"
                                            className="w-full h-full object-cover transition-all group-hover:brightness-75"
                                        />
                                        <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity bg-black bg-opacity-40">
                                            <span className="text-white font-semibold text-lg">Change Picture</span>
                                        </div>
                                    </div>
                                    <input
                                        ref={fileInputRef}
                                        type="file"
                                        accept="image/*"
                                        onChange={handleImageUpload}
                                        className="hidden"
                                    />
                                    <p className="text-sm text-gray-500 mt-2 text-center">Click to upload (max 5MB)</p>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </Fragment>
    );
}
