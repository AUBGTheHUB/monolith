import * as React from 'react';
import { FormProvider, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

import { FirstRegisterFields } from './components/FirstRegisterFields.tsx';
import { SecondRegisterFields } from './components/SecondRegisterFields.tsx';
import { useNavigate } from 'react-router';
import { registerSchema, RegisterFormData } from './validation/validation.tsx';
import { Button } from '@/components/ui/button.tsx';
import { cn } from '@/lib/utils.ts';
import { useMutation } from '@tanstack/react-query';
import { apiClient } from '@/services/apiClient.ts';
import { HubAdmin } from '@/types/hub-admin.ts';

export function RegisterForm() {
    const navigate = useNavigate();
    const [formError, setFormError] = React.useState<string | null>(null);

    const form = useForm<RegisterFormData>({
        resolver: zodResolver(registerSchema),
        defaultValues: {
            username: '',
            password: '',
            repeat_password: '',
            name: '',
            position: '',
            department: '',
            avatar_url: '',
            linkedin: '',
            github: '',
            website: '',
        },
        mode: 'onSubmit',
    });
    const { control, handleSubmit, watch } = form;
    const avatar_url = watch('avatar_url');

    const mutation = useMutation({
        mutationFn: (formData: RegisterFormData) => {
            return apiClient.post<HubAdmin, RegisterFormData>('/auth/register', formData);
        },
        onSuccess: async () => {
            navigate('/admin/login');
        },
        onError: (error) => {
            alert(error.message);
        },
    });

    const onSubmit = (values: RegisterFormData) => {
        setFormError(null);
        console.log(values);
        mutation.mutate(values);
    };

    return (
        <div className="w-full flex flex-col items-center font-mont bg-transparent text-gray-200">
            <p className="text-white mb-6 text-xl">Register</p>

            <FormProvider {...form}>
                <form
                    onSubmit={handleSubmit(onSubmit)}
                    className="w-full max-w-[50rem] px-4 py-6 rounded-lg bg-[#000912]"
                >
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
                                {avatar_url ? (
                                    <img
                                        src={avatar_url}
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
                    <div className="min-h-[1.5rem] mt-3 text-center">
                        {formError && <p className="text-sm text-red-600">{formError}</p>}
                    </div>
                </form>
            </FormProvider>
        </div>
    );
}
