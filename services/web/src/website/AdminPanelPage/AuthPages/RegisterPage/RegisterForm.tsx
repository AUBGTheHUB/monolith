import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { toFormData } from '@/helpers/formHelpers.ts';
import { FirstRegisterFields } from './components/FirstRegisterFields.tsx';
import { SecondRegisterFields } from './components/SecondRegisterFields.tsx';
import { Link, useNavigate } from 'react-router';
import { Form } from '@/components/ui/form.tsx';
import { registerSchema, RegisterFormData } from './validation/validation.tsx';
import { Button } from '@/components/ui/button.tsx';
import { cn } from '@/lib/utils.ts';
import { useMutation } from '@tanstack/react-query';
import { apiClient } from '@/services/apiClient.ts';
import { useMemo } from 'react';

export function RegisterForm() {
    const navigate = useNavigate();

    const form = useForm<RegisterFormData>({
        resolver: zodResolver(registerSchema),
        defaultValues: {
            username: '',
            password: '',
            repeat_password: '',
            name: '',
            avatar: undefined,
        },
        mode: 'onTouched',
    });
    const { control, handleSubmit, watch } = form;
    // Watch the logo field (which is now a FileList)
    const avatarFile = watch('avatar');

    // Create a local preview URL
    const previewUrl = useMemo(() => {
        // 1. If user just selected a NEW file, show that preview
        if (avatarFile instanceof FileList && avatarFile.length > 0) {
            return URL.createObjectURL(avatarFile[0]);
        }

        return null;
    }, [avatarFile]);

    const mutation = useMutation({
        mutationFn: (formData: FormData) => {
            return apiClient.postForm<undefined>('/auth/register', formData);
        },
        onSuccess: async () => {
            navigate('/auth/login');
        },
        onError: (error) => {
            alert(error.message);
        },
    });

    const onSubmit = (values: RegisterFormData) => {
        const formData = toFormData(values);
        mutation.mutate(formData);
    };

    return (
        <div className="w-full flex flex-col items-center font-mont bg-transparent text-gray-200">
            <p className="text-white mb-6 text-xl">Register</p>

            <Form {...form}>
                <form onSubmit={handleSubmit(onSubmit, (errors) => console.log('Validation Errors:', errors))}>
                    <div className="grid sm:grid-cols-2 gap-4 pb-4">
                        <div>
                            <FirstRegisterFields control={control} />
                        </div>
                        <div className="flex-1 flex flex-col items-center justify-start gap-2">
                            <span className={'self-start sm:self-center !text-white'}>Preview</span>

                            <div
                                className={
                                    'relative w-full sm:max-w-[300px] aspect-square rounded-lg flex items-center justify-center overflow-hidden'
                                }
                            >
                                {previewUrl ? (
                                    <img
                                        src={previewUrl}
                                        alt="Preview"
                                        className="w-full h-full object-cover"
                                        onError={(e) => {
                                            (e.target as HTMLImageElement).src =
                                                'https://placehold.co/300?text=Invalid+Image';
                                        }}
                                    />
                                ) : (
                                    <p className={cn('px-4 text-center')}>No image URL provided</p>
                                )}
                            </div>
                        </div>
                    </div>

                    <div className="grid sm:grid-cols-2 gap-3">
                        <SecondRegisterFields control={control} />
                    </div>

                    <div className="flex flex-col sm:flex-row justify-center items-center gap-1 m-0 pb-3">
                        <p>Already have an account? </p>
                        <Link className="text-white hover:text-sky-600" to="/auth/login">
                            Login here!
                        </Link>
                    </div>

                    <div className="flex justify-center mt-3">
                        <Button
                            type="submit"
                            disabled={mutation.isPending}
                            className={`text-white border-2 px-14 border-sky-600 rounded-full bg-transparent hover:bg-sky-600 transition-colors duration-500 hover:text-white ${
                                mutation.isPending ? 'bg-gray-500 hover:bg-gray-500 cursor-not-allowed' : ''
                            }`}
                        >
                            {mutation.isPending ? 'Please wait' : 'Register'}
                        </Button>
                    </div>
                </form>
            </Form>
        </div>
    );
}
