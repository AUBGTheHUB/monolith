import { Fragment, useState, useEffect, useRef } from 'react';
import { useParams, useNavigate, Link } from 'react-router';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Helmet } from 'react-helmet';
import { toast } from 'react-toastify';
import { Plus, X } from 'lucide-react';
import teamMembers from './resources/teamMembers.json';

const AVAILABLE_DEPARTMENTS = [
    'Development',
    'Design',
    'Marketing',
    'PR',
    'Logistics',
    'Board (President)',
    'Board (Vice President)',
    'Board (Treasurer)',
];
// default placeholder image if one isnt uploaded
const DEFAULT_PLACEHOLDER = 'placeholderPic.jpg';

export function EditMemberPage() {
    // get id from url params
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const member = teamMembers.find((m) => m.id === id);
    const fileInputRef = useRef<HTMLInputElement>(null);

    // form state
    const [formData, setFormData] = useState({
        name: '',
        image: DEFAULT_PLACEHOLDER,
    });
    const [imagePreview, setImagePreview] = useState<string>(DEFAULT_PLACEHOLDER);
    const [departments, setDepartments] = useState<string[]>(['']);
    const [errors, setErrors] = useState<Record<string, string>>({});

    // populate form when member data is available
    useEffect(() => {
        if (member) {
            setFormData({
                name: member.name,
                image: member.image || DEFAULT_PLACEHOLDER,
            });
            setImagePreview(member.image || DEFAULT_PLACEHOLDER);
            setDepartments(member.departments.length > 0 ? member.departments : ['']);
        }
    }, [member]);

    // get departments that arent already selected
    const getAvailableDepartments = (currentIndex: number) => {
        const selectedDepts = departments.filter((dept, idx) => idx !== currentIndex && dept !== '');
        return AVAILABLE_DEPARTMENTS.filter((dept) => !selectedDepts.includes(dept));
    };

    // update department selection
    const handleDepartmentChange = (index: number, value: string) => {
        const newDepartments = [...departments];
        newDepartments[index] = value;
        setDepartments(newDepartments);
    };

    // add a new department dropdown
    const addDepartment = () => {
        // Allow adding departments until all are selected
        const validDepartments = departments.filter((dept) => dept !== '');
        if (validDepartments.length < AVAILABLE_DEPARTMENTS.length) {
            setDepartments([...departments, '']);
        }
    };

    // remove a department dropdown
    const removeDepartment = (index: number) => {
        if (departments.length > 1) {
            const newDepartments = departments.filter((_, idx) => idx !== index);
            setDepartments(newDepartments);
        }
    };

    const handleImageClick = () => {
        fileInputRef.current?.click();
    };

    const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            // Validate file type
            if (!file.type.startsWith('image/')) {
                toast.error('Please upload an image file');
                return;
            }

            // File size < 5MB because local storage limits i guess, change if needed
            if (file.size > 5 * 1024 * 1024) {
                toast.error('Image size should be less than 5MB');
                return;
            }

            // Image preview
            const reader = new FileReader();
            reader.onloadend = () => {
                const imageUrl = reader.result as string;
                setImagePreview(imageUrl);

                // in production, upload to server and get the URL

                // const imagePath = `/resources/${file.name}`;
                // setFormData({ ...formData, image: imagePath });

                toast.success('Image uploaded successfully!');
            };
            reader.readAsDataURL(file);
        }
    };

    const validate = () => {
        const newErrors: Record<string, string> = {};

        // Name validation
        if (!formData.name.trim()) {
            newErrors.name = 'Name is required';
        } else if (formData.name.length < 2) {
            newErrors.name = 'Name must be at least 2 characters';
        } else if (formData.name.length > 50) {
            newErrors.name = 'Name must be less than 50 characters';
        }

        // Departments validation
        const validDepartments = departments.filter((dept) => dept !== '');
        if (validDepartments.length === 0) {
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

        const validDepartments = departments.filter((dept) => dept !== '');

        // replace with actual API call when backend is ready
        console.log('Updating team member:', { id, ...formData, departments: validDepartments });

        toast.success('Team member updated successfully!');
        navigate('/dashboard/meet-the-team');
    };

    // if member not found, show error page
    if (!member) {
        return (
            <div className="min-h-screen bg-gray-50 p-8">
                <div className="max-w-2xl mx-auto">
                    <Card>
                        <CardContent className="pt-6">
                            <p className="text-red-500 mb-4">Team member not found</p>
                            <Link to="/dashboard/meet-the-team">
                                <Button className="mt-4 bg-blue-600 justify-center ">Back to Team</Button>
                            </Link>
                        </CardContent>
                    </Card>
                </div>
            </div>
        );
    }

    // Check if we can add more departments
    const validDepartments = departments.filter((dept) => dept !== '');
    const canAddMore = validDepartments.length < AVAILABLE_DEPARTMENTS.length;

    return (
        <Fragment>
            <Helmet>
                <title>Edit Team Member - Admin Panel</title>
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
                            <CardTitle className="text-3xl">Edit Team Member</CardTitle>
                            <p className="text-gray-600 mt-2">Update {member.name}&apos;s profile</p>
                        </CardHeader>
                        <CardContent>
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                {/* Edit Form */}
                                <div className="md:col-span-2">
                                    <form onSubmit={handleSubmit} className="space-y-6">
                                        {/* Name Field */}
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
                                            <div className="space-y-3 mt-2">
                                                {departments.map((dept, index) => (
                                                    <div key={index} className="flex gap-2 items-center">
                                                        {/* Dropdown for departments */}
                                                        <Select
                                                            value={dept}
                                                            onValueChange={(value) =>
                                                                handleDepartmentChange(index, value)
                                                            }
                                                        >
                                                            <SelectTrigger className="flex-1 h-11 border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all">
                                                                <SelectValue placeholder="Select a department" />
                                                            </SelectTrigger>
                                                            <SelectContent className="bg-white border-gray-200 shadow-lg">
                                                                {getAvailableDepartments(index).map((department) => (
                                                                    <SelectItem
                                                                        key={department}
                                                                        value={department}
                                                                        className="cursor-pointer hover:bg-blue-50 focus:bg-blue-100 py-2.5 px-3 transition-colors"
                                                                        // className="cursor-pointer hover:bg-blue-50 focus:bg-blue-100 py-2.5 px-3 transition-colors [&>span:first-child]:order-2 [&>span:first-child]:ml-auto [&>span:last-child]:order-1"
                                                                    >
                                                                        {department}
                                                                    </SelectItem>
                                                                ))}
                                                            </SelectContent>
                                                        </Select>

                                                        {/* Add Department Dropdown Button */}
                                                        {index === departments.length - 1 &&
                                                            dept !== '' &&
                                                            canAddMore && (
                                                                <Button
                                                                    type="button"
                                                                    variant="outline"
                                                                    size="icon"
                                                                    onClick={addDepartment}
                                                                    className="shrink-0 h-11 w-11 border-gray-300 hover:bg-blue-50 hover:border-blue-400 transition-all"
                                                                    title="Add another department"
                                                                >
                                                                    <Plus className="h-4 w-4" />
                                                                </Button>
                                                            )}

                                                        {/* Remove Department Dropdown Button */}
                                                        {departments.length > 1 && (
                                                            <Button
                                                                type="button"
                                                                variant="outline"
                                                                size="icon"
                                                                onClick={() => removeDepartment(index)}
                                                                className="shrink-0 h-11 w-11 border-gray-300 hover:bg-red-50 hover:border-red-400 transition-all"
                                                                title="Remove this department"
                                                            >
                                                                <X className="h-4 w-4 text-red-600" />
                                                            </Button>
                                                        )}
                                                    </div>
                                                ))}
                                            </div>
                                            {errors.departments && (
                                                <p className="text-red-500 text-sm mt-1">{errors.departments}</p>
                                            )}
                                            {/* Show how many departments are selected from the list */}
                                            {/* <p className="text-sm text-gray-500 mt-2">
                                                Selected {validDepartments.length} of {AVAILABLE_DEPARTMENTS.length}{' '}
                                                departments
                                            </p> */}
                                        </div>

                                        <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700">
                                            Update Member
                                        </Button>
                                    </form>
                                </div>

                                {/* Image Preview */}
                                <div className="md:col-span-1">
                                    <Label className="mb-2 block">Profile Picture</Label>
                                    {/* Change Profile Picture - click to upload */}
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
                                    {/* File input for the picture */}
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
