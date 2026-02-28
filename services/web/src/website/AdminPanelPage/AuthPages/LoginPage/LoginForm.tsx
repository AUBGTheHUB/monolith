import * as React from 'react';
import { FormProvider, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { jwtDecode } from 'jwt-decode';

import { Button } from '@/components/ui/button';
import { LoginFormData, loginSchema } from './validation/validation';
import LoginFields from './components/LoginFields';
import { useMutation } from '@tanstack/react-query';
import { useNavigate } from 'react-router';
import { apiClient } from '@/services/apiClient';
import { AuthenticatedAdmin, User } from '@/types/auth';
import { useAuthStore } from '@/hooks/useAuthStote';

export function LoginForm() {
    const navigate = useNavigate();
    const setAuth = useAuthStore((state) => state.setAuth);
    const [formError, setFormError] = React.useState<string | null>(null);

    const form = useForm<LoginFormData>({
        resolver: zodResolver(loginSchema),
        defaultValues: { username: '', password: '' },
        mode: 'onSubmit',
    });

    const { control, handleSubmit } = form;

    const mutation = useMutation({
        mutationFn: (formData: LoginFormData) => {
            return apiClient.post<AuthenticatedAdmin, LoginFormData>('/auth/login', formData);
        },
        onSuccess: async (authData) => {
            const user = jwtDecode<User>(authData.id_token);
            setAuth(authData.access_token, authData.id_token, user);
            console.log(user);
            navigate('/admin/dashboard');
        },
        onError: (error) => {
            alert(error.message);
        },
    });

    const onSubmit = async (values: LoginFormData) => {
        setFormError(null);
        mutation.mutate(values);
    };

    return (
        <div className="w-full flex flex-col items-center font-mont bg-transparent text-gray-200">
            <p className="text-white mb-6 text-xl">Login</p>

            <FormProvider {...form}>
                <form
                    onSubmit={handleSubmit(onSubmit)}
                    className="w-full max-w-[22rem] px-4 py-6 rounded-lg bg-[#000912]"
                >
                    <div className="grid gap-1">
                        <LoginFields control={control} />
                    </div>

                    <div className="flex justify-center mt-3">
                        <Button
                            type="submit"
                            disabled={mutation.isPending}
                            className={`text-white border-2 px-14 border-sky-600 rounded-full bg-transparent hover:bg-sky-600 transition-colors duration-500 hover:text-white ${
                                mutation.isPending ? 'bg-gray-500 hover:bg-gray-500 cursor-not-allowed' : ''
                            }`}
                        >
                            {mutation.isPending ? 'Please wait' : 'Login'}
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
