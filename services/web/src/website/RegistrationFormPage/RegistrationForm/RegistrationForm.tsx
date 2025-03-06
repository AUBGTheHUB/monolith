//to do:  handle is loading etc.., design, design for button for sending emails

import { FormProvider, useForm, useWatch } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { RadioComponent } from '@/internal_library/RadioComponent/RadioComponent';
import { Button } from '@/components/ui/button';
import { InputComponent } from '@/internal_library/InputComponent/InputComponent';
import { DropdownComponent } from '@/internal_library/DropdownComponent/DropdownComponent';
import { registrationSchema } from './schema';
import {
    LEVEL_OPTIONS,
    PROGRAMMING_LANGUAGE_OPTIONS,
    RADIO_OPTIONS,
    REFERRAL_OPTIONS,
    REGISTRATION_TYPE_OPTIONS,
    RegistrationInfo,
    ResendEmailType,
    TSHIRT_OPTIONS,
    UNIVERSITY_OPTIONS,
} from './constants';
import { API_URL } from '@/constants';
import { useEffect, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { jwtDecode } from 'jwt-decode';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

interface DecodedToken {
    sub: string;
    team_id: string;
    team_name: string;
    exp: number;
}

async function registerParticipant(data: RegistrationInfo, token?: string) {
    let response;
    let params;

    if (token) {
        params = new URLSearchParams();
        params.set('jwt_token', token);
    }

    try {
        response = await fetch(`${API_URL}/hackathon/participants?${params?.toString()}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
    } catch {
        throw new Error('Registaration failed, try refreshing the page or contact us.');
    }
    const responseData = await response.json();
    if (!response.ok) {
        throw new Error(
            (responseData && responseData.error) || 'Registaration failed, try refreshing the page or contact us.',
        );
    }
    return responseData.participant?.id;
}

function resendEmail(data: ResendEmailType) {
    fetch(`${API_URL}/hackathon/participants/verify/send-email`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
}

export default function RegistrationForm() {
    const [formData, setFormData] = useState<RegistrationInfo | null>(null);

    const params = new URLSearchParams(window.location.search);

    const token = params.get('jwt_token') ?? undefined;

    const decodedToken: DecodedToken | null = token ? jwtDecode<DecodedToken>(token) : null;

    const [canResendEmail, setCanResendEmail] = useState(false);
    const [resendTimerStart, setResendTimerStart] = useState<number | null>(null);

    useEffect(() => {
        const timerId = setTimeout(() => {
            setCanResendEmail(true);
        }, 90000);
        return () => clearTimeout(timerId);
    }, []);

    const { data, isLoading, isError, error } = useQuery({
        queryKey: ['registerParticipant', formData],
        queryFn: () => registerParticipant(formData!, token),
        enabled: !!formData,
        retry: 1,
        refetchOnWindowFocus: false,
    });

    let formFeedback;
    if (isLoading) {
        formFeedback = <p>Loading...</p>;
    } else if (isError && error instanceof Error) {
        formFeedback = <p>Error: {error.message}</p>;
    } else if (!token) {
        formFeedback = <p>Invalid registration link</p>;
    }

    useEffect(() => {
        console.log('isLoading', isLoading);
        console.log('isError', isError);
        console.log('error', error);
        console.log('data', data);
    }, [isLoading, isError, error, data]);

    const form = useForm<z.infer<typeof registrationSchema>>({
        resolver: zodResolver(registrationSchema),
        defaultValues: {
            name: '',
            email: '',
            tshirt_size: '',
            university: '',
            location: '',
            age: 0,
            source_of_referral: '',
            programming_language: '',
            programming_level: undefined,
            has_participated_in_hackaubg: undefined,
            has_internship_interest: undefined,
            has_participated_in_hackathons: undefined,
            has_previous_coding_experience: undefined,
            share_info_with_sponsors: undefined,
            registration_type: decodedToken?.team_name ? 'invite_link' : undefined,
            team_name: decodedToken?.team_name ?? '',
        },
    });

    const onSubmit = (data: z.infer<typeof registrationSchema>) => {
        console.log('Form submitted:', data);

        if (data.registration_type === 'random') {
            delete data.team_name;
        }

        const wrapData: RegistrationInfo = {
            registration_info: {
                ...data,
                ...((data.registration_type === 'admin' && { is_admin: true }) ||
                    (data.registration_type === 'invite_link' && { is_admin: false })),
            },
        };

        setFormData(wrapData);
    };

    useEffect(() => {
        if (!canResendEmail && resendTimerStart !== null) {
            const timerId = setInterval(() => {
                const now = Date.now();
                const secondsLeft = 90 - Math.floor((now - resendTimerStart) / 1000);
                if (secondsLeft <= 0) {
                    clearInterval(timerId);
                    setCanResendEmail(true);
                }
            }, 1000);
            return () => clearInterval(timerId);
        }
    }, [canResendEmail, resendTimerStart]);

    const onResendEmail = () => {
        if (canResendEmail) {
            const wrappedEmailData: ResendEmailType = { participant_id: data };
            resendEmail(wrappedEmailData);
            setCanResendEmail(false);
            setResendTimerStart(Date.now());
            setTimeout(() => {
                setCanResendEmail(true);
            }, 90000);
        } else {
            if (resendTimerStart) {
                const secondsLeft = 90 - Math.floor((Date.now() - resendTimerStart) / 1000);
                toast.info(`Please wait ${secondsLeft} seconds before trying again.`, {
                    position: 'top-right',
                    autoClose: 5000,
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                });
            }
        }
    };

    const isAdmin = useWatch({
        control: form.control,
        name: 'registration_type',
    });

    useEffect(() => {
        if (isAdmin === 'random') {
            form.clearErrors('team_name');
            form.setValue('team_name', '');
        }
    }, [isAdmin]);

    return (
        <div className="w-full flex flex-col items-center font-mont bg-[#000912] relative text-gray-400">
            <div className="w-4/5 flex items-start mb-24 mt-16">
                <img src="/RegistrationForm/s.png" alt="" className="w-[1.6rem] mt-3" />
                <p className="text-white ml-5 tracking-[0.2em] text-3xl sm:text-4xl">REGISTER</p>
            </div>
            <div className="flex justify-center w-full">
                <FormProvider {...form}>
                    <form
                        onSubmit={form.handleSubmit(onSubmit)}
                        className="bg-[#000912] w-full max-w-5xl p-6 border border-gray-700 rounded-lg shadow-md"
                    >
                        <div className="">
                            <div>
                                <p className="text-lg font-semibold mb-2 mt-16">Personal Info</p>
                                <hr className="mb-8" />
                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                                    <InputComponent
                                        control={form.control}
                                        name="name"
                                        label="Name"
                                        type="text"
                                        placeholder="Enter your name"
                                    />
                                    <InputComponent
                                        control={form.control}
                                        name="age"
                                        label="Age"
                                        type="number"
                                        placeholder="Enter your age"
                                    />
                                    <InputComponent
                                        control={form.control}
                                        name="email"
                                        label="Email"
                                        type="email"
                                        placeholder="Enter your email"
                                    />
                                    <InputComponent
                                        control={form.control}
                                        name="location"
                                        label="Location"
                                        type="text"
                                        placeholder="Enter your location"
                                    />
                                    <DropdownComponent
                                        control={form.control}
                                        name="university"
                                        label="University"
                                        placeholder="Select your university"
                                        items={UNIVERSITY_OPTIONS.map(({ label, value }) => ({ name: label, value }))}
                                    />
                                </div>
                            </div>
                            <div>
                                <p className="text-lg font-semibold mt-16 mb-2">Participation</p>
                                <hr className="mb-8" />
                                <div className="grid ">
                                    <div className="grid grid-cols-2 gap-6">
                                        <DropdownComponent
                                            control={form.control}
                                            name="tshirt_size"
                                            label="T-Shirt Size"
                                            placeholder="Select your size"
                                            items={TSHIRT_OPTIONS.map(({ label, value }) => ({ name: label, value }))}
                                        />
                                        <DropdownComponent
                                            control={form.control}
                                            name="source_of_referral"
                                            label="Source of Referral"
                                            placeholder="How did you hear about us?"
                                            items={REFERRAL_OPTIONS.map(({ label, value }) => ({ name: label, value }))}
                                        />
                                        <DropdownComponent
                                            control={form.control}
                                            name="programming_language"
                                            label="Programming Language"
                                            placeholder="Select your preferred language"
                                            items={PROGRAMMING_LANGUAGE_OPTIONS.map(({ label, value }) => ({
                                                name: label,
                                                value,
                                            }))}
                                        />
                                    </div>

                                    <div className="grid grid-cols-1">
                                        <RadioComponent
                                            control={form.control}
                                            name="programming_level"
                                            options={LEVEL_OPTIONS}
                                            groupLabel="Programming Level"
                                        />
                                        <RadioComponent
                                            control={form.control}
                                            name="has_participated_in_hackaubg"
                                            options={RADIO_OPTIONS}
                                            groupLabel="Have you participated in HackAUBG before?"
                                        />
                                        <RadioComponent
                                            control={form.control}
                                            name="has_internship_interest"
                                            options={RADIO_OPTIONS}
                                            groupLabel="Are you interested in internships?"
                                        />
                                        <RadioComponent
                                            control={form.control}
                                            name="has_participated_in_hackathons"
                                            options={RADIO_OPTIONS}
                                            groupLabel="Have you participated in hackathons before?"
                                        />
                                        <RadioComponent
                                            control={form.control}
                                            name="has_previous_coding_experience"
                                            options={RADIO_OPTIONS}
                                            groupLabel="Do you have previous coding experience?"
                                        />
                                        <RadioComponent
                                            control={form.control}
                                            name="registration_type"
                                            options={REGISTRATION_TYPE_OPTIONS}
                                            groupLabel="Enter registration type"
                                            disabled={decodedToken?.team_name ? true : false}
                                        />
                                        <InputComponent
                                            control={form.control}
                                            name="team_name"
                                            label="Team Name"
                                            type="text"
                                            placeholder="Enter your team name"
                                            disabled={isAdmin !== 'admin'}
                                        />
                                        <RadioComponent
                                            control={form.control}
                                            name="share_info_with_sponsors"
                                            options={[
                                                { label: 'Yes', value: true },
                                                { label: 'No', value: false },
                                            ]}
                                            groupLabel="Do you agree to share your info with sponsors?"
                                        />

                                        <img src="/AwardsSection/line.svg" alt="Divider" className="w-full h-auto" />
                                    </div>
                                </div>
                            </div>
                            <div className="flex justify-start mt-4">
                                <Button
                                    type="submit"
                                    className="mt-10 text-white border-2 border-sky-600 rounded-full bg-transparent hover:bg-sky-600 transition-colors duration-500 hover:text-white"
                                >
                                    Participate now
                                </Button>
                            </div>
                            {data && (
                                <p
                                    onClick={onResendEmail}
                                    style={{
                                        cursor: canResendEmail ? 'pointer' : 'not-allowed',
                                    }}
                                >
                                    Did not receive an email? Click here.
                                </p>
                            )}
                        </div>
                        <div>{formFeedback}</div>
                    </form>
                </FormProvider>
            </div>
            <ToastContainer
                position="top-right"
                autoClose={5000}
                hideProgressBar={false}
                newestOnTop={false}
                closeOnClick={true}
                rtl={false}
                pauseOnFocusLoss={true}
                draggable={true}
                pauseOnHover={true}
                aria-label="Notification"
            />
        </div>
    );
}
