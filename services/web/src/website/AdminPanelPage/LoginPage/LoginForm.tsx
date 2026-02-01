import * as React from 'react';
import { FormProvider, useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';

import { InputComponent } from '@/internalLibrary/InputComponent/InputComponent';
import { Button } from '@/components/ui/button';

import { validateAdminCredentials } from '@/website/AdminPanelPage/LoginPage/mockAdmins';
import { useNavigate } from 'react-router';

const loginSchema = z.object({
    email: z.string().email('Please enter a valid email'),
    password: z.string().min(6, 'Password must be at least 6 characters'),
});

type LoginValues = z.infer<typeof loginSchema>;

export function LoginForm() {
    const navigate = useNavigate();
    const [formError, setFormError] = React.useState<string | null>(null);

    const form = useForm<LoginValues>({
        resolver: zodResolver(loginSchema),
        defaultValues: { email: '', password: '' },
        mode: 'onSubmit',
    });

    const onSubmit = (values: LoginValues) => {
        setFormError(null);

        const res = validateAdminCredentials(values.email, values.password);
        if (!res.ok) {
            setFormError(res.reason);
            return;
        }

        localStorage.setItem('hub_admin_auth', '1');
        navigate('/dashboard');
    };

    return (
        <div className="w-full flex flex-col items-center font-mont bg-transparent text-gray-200">
            <p className="text-white mb-6 text-xl">Login</p>

            <FormProvider {...form}>
                <form
                    onSubmit={form.handleSubmit(onSubmit)}
                    className="w-full max-w-[22rem] px-4 py-6 rounded-lg bg-[#000912]"
                >
                    <div className="grid gap-1">
                        <InputComponent
                            control={form.control}
                            name="email"
                            label="Email"
                            type="email"
                            placeholder="Enter your email"
                            labelClassName="text-white"
                            inputClassName="bg-transparent text-[#A6AAB2] border border-[#233340] rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#A6AAB2]"
                        />

                        <InputComponent
                            control={form.control}
                            name="password"
                            label="Password"
                            type="password"
                            placeholder="Enter your password"
                            labelClassName="text-white"
                            inputClassName="bg-transparent text-[#A6AAB2] border border-[#233340] rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#A6AAB2]"
                        />
                    </div>

                    <div className="flex justify-center mt-3">
                        <Button
                            type="submit"
                            disabled={form.formState.isSubmitting}
                            className={`text-white border-2 px-14 border-sky-600 rounded-full bg-transparent hover:bg-sky-600 transition-colors duration-500 hover:text-white ${
                                form.formState.isSubmitting ? 'bg-gray-500 hover:bg-gray-500 cursor-not-allowed' : ''
                            }`}
                        >
                            {form.formState.isSubmitting ? 'Please wait' : 'Login'}
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
