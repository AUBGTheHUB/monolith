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
    REGISTRATION_TYPE_OPTIONS_INV,
    REGISTRATION_TYPE_OPTIONS_NO_INV,
    RegistrationInfo,
    ResendEmailType,
    TSHIRT_OPTIONS,
    UNIVERSITY_OPTIONS,
} from './constants';
import { API_URL } from '@/constants';
import { Fragment, useEffect, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { jwtDecode } from 'jwt-decode';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Loader2 } from 'lucide-react';

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
    const [secondsLeft, setSecondsLeft] = useState(90);
    const [isSubmitted, setIsSubmitted] = useState(false);

    useEffect(() => {
        if (resendTimerStart !== null) {
            const interval = setInterval(() => {
                const elapsedTime = Math.floor((Date.now() - resendTimerStart) / 1000);
                const timeRemaining = 90 - elapsedTime;
                setSecondsLeft(timeRemaining > 0 ? timeRemaining : 0);

                if (timeRemaining <= 0) {
                    setCanResendEmail(true);
                    setResendTimerStart(null);
                    clearInterval(interval);
                }
            }, 1000);
            return () => clearInterval(interval);
        }
    }, [resendTimerStart]);

    const { data, isLoading, isError, error } = useQuery({
        queryKey: ['registerParticipant', formData],
        queryFn: () => registerParticipant(formData!, token),
        enabled: !!formData,
        retry: 1,
        refetchOnWindowFocus: false,
    });

    let formFeedback;
    if (isError && error instanceof Error) {
        formFeedback = <p>{error.message}</p>;
    }

    useEffect(() => {
        if (data) {
            setIsSubmitted(true);
            toast.success('Registration successful', {
                position: 'top-right',
                autoClose: 5000,
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
                className: 'bg-[#000912] text-white',
            });
        }
    }, [data]);

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

    const registrationType = useWatch({
        control: form.control,
        name: 'registration_type',
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

        setCanResendEmail(false);
        setResendTimerStart(Date.now());
        setSecondsLeft(90);
    };
    const onResendEmail = () => {
        if (!canResendEmail) {
            toast.info(`Please wait ${secondsLeft} seconds before resending.`, {
                position: 'top-right',
                autoClose: 3000,
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
                className: 'bg-[#000912] text-white',
            });
            return;
        }

        const wrappedEmailData: ResendEmailType = { participant_id: data };
        resendEmail(wrappedEmailData);

        setCanResendEmail(false);
        setResendTimerStart(Date.now());
        setSecondsLeft(90);

        toast.success('Verification email has been resent. Please wait 90 seconds before resending again.', {
            position: 'top-right',
            autoClose: 5000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            className: 'bg-[#000912] text-white',
        });
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
        <div className="w-full flex bg-[url('/spaceBg.png')] flex-col items-center font-mont bg-[#000912] relative text-gray-400 min-h-[100vh]">
            <div className="w-11/12 sm:w-4/5 flex items-start mb-20 mt-16">
                <img src="/RegistrationForm/s.png" alt="" className="w-[1.6rem] mt-3" />
                <p className="text-white ml-5 tracking-[0.2em] text-3xl sm:text-4xl">REGISTER</p>
            </div>

            <div className="flex justify-center w-full">
                <FormProvider {...form}>
                    <form
                        onSubmit={form.handleSubmit(onSubmit)}
                        className="relative bg-[#000912] w-full max-w-[90%] sm:max-w-[70%] px-5 sm:px-14 py-8 border border-gray-700 rounded-lg shadow-md mb-16"
                    >
                        <img
                            src="/RegistrationForm/reg_line.svg"
                            alt=""
                            className="absolute top-[-1px] sm:top-[-2px]  w-full h-auto z-10"
                        />
                        <div>
                            <p className="text-white text-lg font-semibold mb-2 mt-12">Personal Info</p>
                            <hr className="mb-8 h-0.5 bg-[#233340] border-0" />
                            <div className="grid grid-cols-1 sm:grid-cols-2 sm:gap-6">
                                <InputComponent
                                    control={form.control}
                                    name="name"
                                    label="Name"
                                    type="text"
                                    placeholder="Enter your name"
                                    labelClassName="text-white"
                                    inputClassName="bg-transparent text-[#A6AAB2] border border-[#233340] rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#A6AAB2]"
                                />
                                <InputComponent
                                    control={form.control}
                                    name="age"
                                    label="Age"
                                    type="number"
                                    placeholder="Enter your age"
                                    labelClassName="text-white"
                                    inputClassName="bg-transparent text-[#A6AAB2] border border-[#233340] rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#A6AAB2]
                                appearance-none [&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none"
                                />
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
                                    name="location"
                                    label="Location"
                                    type="text"
                                    placeholder="Enter your location"
                                    labelClassName="text-white"
                                    inputClassName="bg-transparent text-[#A6AAB2] border border-[#233340] rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#A6AAB2]"
                                />
                                <DropdownComponent
                                    control={form.control}
                                    name="university"
                                    label="University"
                                    placeholder="Select your university"
                                    dropdownLabelClassName="text-white"
                                    selectContentClassName="bg-[#000912] text-white border border-[#233340]"
                                    formControlClassName="bg-[#000912] border border-[#233340]"
                                    items={UNIVERSITY_OPTIONS.map(({ label, value }) => ({ name: label, value }))}
                                />
                            </div>

                            <div>
                                <p className="text-white text-lg font-semibold mt-12 mb-2">Participation</p>
                                <hr className="mb-8 h-0.5 bg-[#233340] border-0" />
                                <div className="grid ">
                                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                                        <DropdownComponent
                                            control={form.control}
                                            name="tshirt_size"
                                            label="T-Shirt Size"
                                            placeholder="Select your size"
                                            dropdownLabelClassName="text-white"
                                            selectContentClassName="bg-[#000912] text-white border border-[#233340]"
                                            formControlClassName="bg-[#000912] border border-[#233340]"
                                            items={TSHIRT_OPTIONS.map(({ label, value }) => ({ name: label, value }))}
                                        />

                                        <DropdownComponent
                                            control={form.control}
                                            name="source_of_referral"
                                            label="Source of Referral"
                                            placeholder="How did you hear about us?"
                                            dropdownLabelClassName="text-white"
                                            selectContentClassName="bg-[#000912] text-white border border-[#233340]"
                                            formControlClassName="bg-[#000912] border border-[#233340]"
                                            items={REFERRAL_OPTIONS.map(({ label, value }) => ({ name: label, value }))}
                                        />
                                        <DropdownComponent
                                            control={form.control}
                                            name="programming_language"
                                            label="Programming Language"
                                            placeholder="Select your preferred language"
                                            dropdownLabelClassName="text-white"
                                            selectContentClassName="bg-[#000912] text-white border border-[#233340]"
                                            formControlClassName="bg-[#000912] border border-[#233340]"
                                            items={PROGRAMMING_LANGUAGE_OPTIONS.map(({ label, value }) => ({
                                                name: label,
                                                value,
                                            }))}
                                        />
                                    </div>

                                    <div className="grid grid-cols-1 sm:grid-cols-2 ">
                                        <RadioComponent
                                            control={form.control}
                                            name="programming_level"
                                            options={LEVEL_OPTIONS}
                                            groupLabel="Programming Level"
                                            groupClassName="text-white"
                                            radioGroupClassName="text-[#A6AAB2]"
                                        />
                                        <RadioComponent
                                            control={form.control}
                                            name="has_participated_in_hackaubg"
                                            options={RADIO_OPTIONS}
                                            groupLabel="Have you participated in HackAUBG before?"
                                            groupClassName="text-white"
                                            radioGroupClassName="text-[#A6AAB2]"
                                        />

                                        <RadioComponent
                                            control={form.control}
                                            name="has_internship_interest"
                                            options={RADIO_OPTIONS}
                                            groupLabel="Are you interested in internships?"
                                            groupClassName="text-white"
                                            radioGroupClassName=" text-[#A6AAB2]"
                                        />
                                        <RadioComponent
                                            control={form.control}
                                            name="has_participated_in_hackathons"
                                            options={RADIO_OPTIONS}
                                            groupLabel="Have you participated in hackathons before?"
                                            groupClassName="text-white"
                                            radioGroupClassName=" text-[#A6AAB2]"
                                        />
                                        <RadioComponent
                                            control={form.control}
                                            name="has_previous_coding_experience"
                                            options={RADIO_OPTIONS}
                                            groupLabel="Do you have previous coding experience?"
                                            groupClassName="text-white"
                                            radioGroupClassName=" text-[#A6AAB2]"
                                        />
                                    </div>
                                    <div className="grid grid-cols-1 sm:grid-cols-2 ">
                                        <RadioComponent
                                            control={form.control}
                                            name="registration_type"
                                            options={
                                                decodedToken
                                                    ? REGISTRATION_TYPE_OPTIONS_INV
                                                    : REGISTRATION_TYPE_OPTIONS_NO_INV
                                            }
                                            groupLabel="Enter registration type"
                                            disabled={decodedToken?.team_name ? true : false}
                                            groupClassName="text-white"
                                            radioGroupClassName="text-[#A6AAB2]"
                                        />

                                        <InputComponent
                                            control={form.control}
                                            name="team_name"
                                            label="Team Name"
                                            type="text"
                                            placeholder="Enter your team name"
                                            disabled={isAdmin !== 'admin'}
                                            labelClassName="text-white"
                                            inputClassName="bg-transparent text-[#A6AAB2] border border-[#233340] rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-[#A6AAB2]"
                                        />
                                        <RadioComponent
                                            control={form.control}
                                            name="share_info_with_sponsors"
                                            options={[
                                                { label: 'Yes', value: true },
                                                { label: 'No', value: false },
                                            ]}
                                            groupLabel="Do you agree to share your info with sponsors?"
                                            groupClassName="text-white"
                                            radioGroupClassName=" text-[#A6AAB2]"
                                        />
                                    </div>
                                    <img src="/AwardsSection/line.svg" alt="Divider" className="w-full h-auto" />
                                </div>
                            </div>
                            <div className="flex justify-start mt-4">
                                <Button
                                    disabled={isLoading || isSubmitted}
                                    type="submit"
                                    className={`mt-10 text-white border-2 border-sky-600 rounded-full bg-transparent hover:bg-sky-600 transition-colors duration-500 hover:text-white ${
                                        isLoading || isSubmitted
                                            ? 'bg-gray-500 hover:bg-gray-500 cursor-not-allowed'
                                            : ''
                                    }`}
                                >
                                    {isLoading ? (
                                        <Fragment>
                                            <Loader2 className="animate-spin" />
                                            Please wait
                                        </Fragment>
                                    ) : (
                                        'Participate now'
                                    )}
                                </Button>
                            </div>
                            {data && registrationType !== 'invite_link' && (
                                <p className="text-[#A6AAB2] mt-4 text-sm">
                                    Did not receive an email?{' '}
                                    <span
                                        onClick={onResendEmail}
                                        className={`underline ${
                                            canResendEmail
                                                ? 'cursor-pointer text-white hover:text-[#A6AAB2] transition duration-200'
                                                : 'cursor-not-allowed text-gray-500'
                                        }`}
                                    >
                                        Click here
                                    </span>{' '}
                                    {canResendEmail ? '' : `(Wait ${secondsLeft}s)`}
                                </p>
                            )}
                        </div>
                        <div className="text-sm text-red-600 mt-4">{formFeedback}</div>
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
