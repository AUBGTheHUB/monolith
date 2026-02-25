import flameTL from './images/flame_TL.png';
import flameBR from './images/flame_BR.png';
import { FormProvider, useForm, useWatch } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { RadioComponent } from '@/internalLibrary/RadioComponent/RadioComponent';
import { Button } from '@/components/ui/button';
import { InputComponent } from '@/internalLibrary/InputComponent/InputComponent';
import { DropdownComponent } from '@/internalLibrary/DropdownComponent/DropdownComponent';
import { registrationSchema } from './schema';
import {
    LEVEL_OPTIONS,
    PROGRAMMING_LANGUAGE_OPTIONS,
    RADIO_OPTIONS,
    REFERRAL_OPTIONS,
    REGISTRATION_TYPE_OPTIONS_INV,
    REGISTRATION_TYPE_OPTIONS_NO_INV,
    TSHIRT_OPTIONS,
    UNIVERSITY_OPTIONS,
} from './constants';
import type { RegistrationInfo } from './constants';
import { useEffect, useMemo, useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { jwtDecode } from 'jwt-decode';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Loader2 } from 'lucide-react';

import { registerParticipant, resendEmail } from './api';
import { DecodedToken, RESEND_COOLDOWN_SECONDS, registrationMessage } from './config';
import { useCooldownTimer } from './useCooldownTimer';
import {
    labelStyles,
    inputStyles,
    numberInputOverrides,
    radioGroupStyles,
    dropdownLabelStyles,
    selectContentStyles,
    formControlStyles,
    sectionHeadingStyles,
    sectionDividerStyles,
    fieldGridStyles,
    fieldGridWithMarginStyles,
    formCardStyles,
    submitButtonStyles,
    resendButtonStyles,
    errorTextStyles,
} from './styles';

const toDropdownItems = (options: { label: string; value: string }[]) =>
    options.map(({ label, value }) => ({ name: label, value }));

interface RegistrationFormProps {
    RegSwitch: boolean;
    isRegTeamsFull: boolean;
}

export default function RegistrationForm({ RegSwitch, isRegTeamsFull }: RegistrationFormProps) {
    const params = new URLSearchParams(window.location.search);
    const token = params.get('jwt_token') ?? undefined;
    const decodedToken = useMemo<DecodedToken | null>(
        () => (token ? jwtDecode<DecodedToken>(token) : null),
        [token],
    );

    const [isSubmitted, setIsSubmitted] = useState(false);
    const [fadeIn, setFadeIn] = useState(false);
    const cooldown = useCooldownTimer(RESEND_COOLDOWN_SECONDS);

    useEffect(() => {
        const timer = setTimeout(() => setFadeIn(true), 100);
        return () => clearTimeout(timer);
    }, []);

    const {
        mutate,
        data: participantId,
        isPending,
        isError,
        error,
    } = useMutation({
        mutationFn: (formData: RegistrationInfo) => registerParticipant(formData, token),
        retry: 1,
        onSuccess: () => {
            setIsSubmitted(true);
            cooldown.start();
            toast.success('Registration successful', {
                position: 'top-right',
                autoClose: 5000,
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
                className: 'bg-white text-black border border-gray-200',
            });
        },
    });

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
        if (data.registration_type === 'random') {
            delete data.team_name;
        }

        const payload: RegistrationInfo = {
            registration_info: {
                ...data,
                ...((data.registration_type === 'admin' && { is_admin: true }) ||
                    (data.registration_type === 'invite_link' && { is_admin: false })),
            },
        };

        mutate(payload);
    };

    const resendMutation = useMutation({
        mutationFn: () => resendEmail({ participant_id: participantId! }),
        onSuccess: () => {
            cooldown.start();
            toast.success('Verification email resent.', {
                position: 'top-right',
                autoClose: 5000,
                className: 'bg-white text-black',
            });
        },
        onError: (err) => {
            toast.error(err instanceof Error ? err.message : 'Failed to resend email.', {
                position: 'top-right',
                autoClose: 5000,
                className: 'bg-white text-black',
            });
        },
    });

    const onResendEmail = () => {
        if (cooldown.isCoolingDown) {
            toast.info(`Please wait ${cooldown.secondsLeft} seconds before resending.`, {
                position: 'top-right',
                autoClose: 3000,
                className: 'bg-white text-black',
            });
            return;
        }
        resendMutation.mutate();
    };

    useEffect(() => {
        if (registrationType === 'random') {
            form.clearErrors('team_name');
            form.setValue('team_name', '');
        }
    }, [registrationType]);

    const isFormDisabled = isPending || isSubmitted;

    if (!RegSwitch || (isRegTeamsFull && registrationType !== 'invite_link')) {
        return (
            <div
                className={`w-full flex flex-col items-center overflow-hidden font-mont bg-white relative text-gray-800 min-h-screen transition-opacity duration-1000 pt-24 ${fadeIn ? 'opacity-100' : 'opacity-0'}`}
            >
                <div className="w-11/12 sm:w-4/5 flex justify-center mb-10 mt-16 z-10">
                    <p className="text-black tracking-[0.5em] text-4xl sm:text-5xl font-light">REGISTER</p>
                </div>
                <div className="h-[45vh] flex w-[80%] justify-center items-center z-10">
                    <div className="bg-white/80 backdrop-blur-md h-full rounded-3xl w-full border border-gray-200 shadow-xl flex justify-center items-center font-mont text-2xl">
                        <p className="text-center p-5 text-gray-800">{registrationMessage}</p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div
            className={`w-full flex flex-col items-center overflow-x-hidden font-mont bg-[#fafafa] relative text-gray-800 min-h-screen transition-opacity duration-1000 pt-24 ${fadeIn ? 'opacity-100' : 'opacity-0'}`}
        >
            <img
                src={flameTL}
                alt=""
                className="absolute top-0 left-0 w-[800px] opacity-90 z-0 pointer-events-none mix-blend-multiply"
            />
            <img
                src={flameBR}
                alt=""
                className="absolute bottom-0 right-0 w-[800px] opacity-90 z-0 pointer-events-none mix-blend-multiply"
            />

            <div className="w-11/12 sm:w-4/5 flex justify-center mb-12 mt-16 z-10">
                <p className="text-gray-900 tracking-[0.4em] text-3xl sm:text-4xl font-medium uppercase">REGISTER</p>
            </div>

            <div className="flex justify-center w-full z-10">
                <FormProvider {...form}>
                    <form
                        onSubmit={form.handleSubmit(onSubmit)}
                        className={formCardStyles}
                    >
                        <div>
                            <p className={`${sectionHeadingStyles} mt-4`}>Personal Info</p>
                            <hr className={sectionDividerStyles} />

                            <div className={fieldGridStyles}>
                                <InputComponent
                                    control={form.control}
                                    name='name'
                                    label="Name"
                                    type="text"
                                    placeholder="Enter your name"
                                    labelClassName={labelStyles}
                                    inputClassName={inputStyles} 
                                />
                                <InputComponent
                                    control={form.control}
                                    name="age"
                                    label="Age"
                                    type="number"
                                    placeholder="Enter your age"
                                    labelClassName={labelStyles}
                                    inputClassName={`${inputStyles} ${numberInputOverrides}`}
                                />
                                <InputComponent
                                    control={form.control}
                                    name="email"
                                    label="Email"
                                    type="email"
                                    placeholder="Enter your email"
                                    labelClassName={labelStyles}
                                    inputClassName={inputStyles}
                                />
                                <InputComponent
                                    control={form.control}
                                    name="location"
                                    label="Location"
                                    type="text"
                                    placeholder="Enter your city and country"
                                    labelClassName={labelStyles}
                                    inputClassName={inputStyles}
                                />
                                <DropdownComponent
                                    control={form.control}
                                    name="university"
                                    label="University"
                                    placeholder="Select your university"
                                    dropdownLabelClassName={dropdownLabelStyles}
                                    selectContentClassName={selectContentStyles}
                                    formControlClassName={formControlStyles}
                                    items={toDropdownItems(UNIVERSITY_OPTIONS)}
                                />
                            </div>
                        </div>

                        <div>
                            <p className={`${sectionHeadingStyles} mt-8 sm:mt-12`}>Participation</p>
                            <hr className={sectionDividerStyles} />

                            <div className={fieldGridStyles}>
                                <DropdownComponent
                                    control={form.control}
                                    name="tshirt_size"
                                    label="T-Shirt Size"
                                    placeholder="Select your size"
                                    dropdownLabelClassName={dropdownLabelStyles}
                                    selectContentClassName={selectContentStyles}
                                    formControlClassName={formControlStyles}
                                    items={toDropdownItems(TSHIRT_OPTIONS)}
                                />
                                <DropdownComponent
                                    control={form.control}
                                    name="source_of_referral"
                                    label="Source of Referral"
                                    placeholder="How did you hear about us?"
                                    dropdownLabelClassName={dropdownLabelStyles}
                                    selectContentClassName={selectContentStyles}
                                    formControlClassName={formControlStyles}
                                    items={toDropdownItems(REFERRAL_OPTIONS)}
                                />
                            </div>

                            <div className={fieldGridWithMarginStyles}>
                                <DropdownComponent
                                    control={form.control}
                                    name="programming_language"
                                    label="Programming Language"
                                    placeholder="Select your preferred language"
                                    dropdownLabelClassName={dropdownLabelStyles}
                                    selectContentClassName={selectContentStyles}
                                    formControlClassName={formControlStyles}
                                    items={toDropdownItems(PROGRAMMING_LANGUAGE_OPTIONS)}
                                />
                            </div>

                            <div className={fieldGridWithMarginStyles}>
                                <RadioComponent
                                    control={form.control}
                                    name="programming_level"
                                    options={LEVEL_OPTIONS}
                                    groupLabel="Programming Level"
                                    groupClassName={labelStyles}
                                    radioGroupClassName={radioGroupStyles}
                                />
                                <RadioComponent
                                    control={form.control}
                                    name="has_participated_in_hackaubg"
                                    options={RADIO_OPTIONS}
                                    groupLabel="Have you participated in HackAUBG before?"
                                    groupClassName={labelStyles}
                                    radioGroupClassName={radioGroupStyles}
                                />
                            </div>

                            <div className={fieldGridWithMarginStyles}>
                                <RadioComponent
                                    control={form.control}
                                    name="has_internship_interest"
                                    options={RADIO_OPTIONS}
                                    groupLabel="Are you interested in internships?"
                                    groupClassName={labelStyles}
                                    radioGroupClassName={radioGroupStyles}
                                />
                                <RadioComponent
                                    control={form.control}
                                    name="has_participated_in_hackathons"
                                    options={RADIO_OPTIONS}
                                    groupLabel="Have you participated in hackathons before?"
                                    groupClassName={labelStyles}
                                    radioGroupClassName={radioGroupStyles}
                                />
                            </div>

                            <div className={fieldGridWithMarginStyles}>
                                <RadioComponent
                                    control={form.control}
                                    name="has_previous_coding_experience"
                                    options={RADIO_OPTIONS}
                                    groupLabel="Do you have previous coding experience?"
                                    groupClassName={labelStyles}
                                    radioGroupClassName={radioGroupStyles}
                                />
                            </div>

                            <div className={fieldGridWithMarginStyles}>
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
                                    groupClassName={labelStyles}
                                    radioGroupClassName={radioGroupStyles}
                                />
                                <InputComponent
                                    control={form.control}
                                    name="team_name"
                                    label="Team Name"
                                    type="text"
                                    placeholder="Enter your team name"
                                    disabled={registrationType !== 'admin'}
                                    labelClassName={labelStyles}
                                    inputClassName={inputStyles}
                                />
                            </div>

                            <div className={fieldGridWithMarginStyles}>
                                <RadioComponent
                                    control={form.control}
                                    name="share_info_with_sponsors"
                                    options={[
                                        { label: 'Yes', value: true },
                                        { label: 'No', value: false },
                                    ]}
                                    groupLabel="Do you agree to share your info with sponsors?"
                                    groupClassName={labelStyles}
                                    radioGroupClassName={radioGroupStyles}
                                />
                            </div>
                        </div>

                        <div className="flex justify-start mt-8">
                            <Button
                                disabled={isFormDisabled}
                                type="submit"
                                className={`${submitButtonStyles} ${
                                    isFormDisabled ? 'opacity-50 cursor-not-allowed' : ''
                                }`}
                            >
                                {isPending ? (
                                    <>
                                        <Loader2 className="animate-spin mr-2" size={16} />
                                        Please wait
                                    </>
                                ) : (
                                    'Participate now'
                                )}
                            </Button>
                        </div>

                        {isError && error instanceof Error && (
                            <p className={errorTextStyles}>{error.message}</p>
                        )}

                        {isSubmitted && registrationType !== 'invite_link' && (
                            <div className="mt-4">
                                <Button
                                    type="button"
                                    onClick={onResendEmail}
                                    disabled={cooldown.isCoolingDown}
                                    className={resendButtonStyles}
                                >
                                    {cooldown.isCoolingDown
                                        ? `Resend email (${cooldown.secondsLeft}s)`
                                        : 'Resend verification email'}
                                </Button>
                            </div>
                        )}
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
            />
        </div>
    );
}