import flameTL from './flame_TL.png';
import flameBR from './flame_BR.png';
import { FormProvider, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { RadioComponent } from '@/internalLibrary/RadioComponent/RadioComponent';
import { Button } from '@/components/ui/button';
import { InputComponent } from '@/internalLibrary/InputComponent/InputComponent';
import { registrationSchema } from './schema';
import { TRAIT_OPTIONS, ROLE_OPTIONS, RegistrationInfo, ResendEmailType } from './constants';
import { API_URL } from '@/constants';
import { useCallback, useEffect, useRef, useState } from 'react';
import { useMutation } from '@tanstack/react-query';
//import { jwtDecode } from 'jwt-decode';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { Loader2 } from 'lucide-react';

// interface DecodedToken {
//     sub: string;
//     team_id: string;
//     team_name: string;
//     exp: number;
// }

const RESEND_COOLDOWN_SECONDS = 90;
const REGISTRATION_CUTOFF_DATE = new Date('2026-03-14T00:00:00'); //??? This is from last year. I did update it, but don't know the dates

const currentDate = new Date();
const registrationMessage =
    currentDate < REGISTRATION_CUTOFF_DATE ? 'Registration is coming soon...' : 'Registration is closed';

const labelStyles = 'text-gray-700 font-medium text-sm mb-1';
const inputStyles =
    'bg-white text-gray-800 border border-gray-400 rounded-md px-3 py-2 focus:outline-none focus:ring-1 focus:ring-red-400 transition-shadow';
const radioGroupStyles = 'flex flex-wrap gap-4 text-gray-600 text-sm';

async function registerParticipant(data: RegistrationInfo, token?: string): Promise<string> {
    const params = token ? new URLSearchParams({ jwt_token: token }) : undefined;

    let response: Response;
    try {
        response = await fetch(`${API_URL}/hackathon/participants?${params?.toString() ?? ''}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
    } catch {
        throw new Error('Registration failed, try refreshing the page or contact us.');
    }

    const responseData = await response.json();
    if (!response.ok) {
        throw new Error(responseData?.error || 'Registration failed, try refreshing the page or contact us.');
    }

    return responseData.participant?.id;
}

async function resendEmail(data: ResendEmailType): Promise<void> {
    let response: Response;
    try {
        response = await fetch(`${API_URL}/hackathon/participants/verify/send-email`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
    } catch {
        throw new Error('Failed to resend verification email. Please try again.');
    }

    if (!response.ok) {
        throw new Error('Failed to resend verification email.');
    }
}

function useCooldownTimer(durationSeconds: number) {
    const [secondsLeft, setSecondsLeft] = useState(0);
    const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

    const start = useCallback(() => {
        setSecondsLeft(durationSeconds);

        if (intervalRef.current) {
            clearInterval(intervalRef.current);
        }

        intervalRef.current = setInterval(() => {
            setSecondsLeft((prev) => {
                if (prev <= 1) {
                    clearInterval(intervalRef.current!);
                    intervalRef.current = null;
                    return 0;
                }
                return prev - 1;
            });
        }, 1000);
    }, [durationSeconds]);

    useEffect(() => {
        return () => {
            if (intervalRef.current) {
                clearInterval(intervalRef.current);
            }
        };
    }, []);

    const isCoolingDown = secondsLeft > 0;

    return { secondsLeft, isCoolingDown, start };
}

interface RegistrationFormProps {
    RegSwitch: boolean;
    isRegTeamsFull: boolean;
}

export default function RegistrationForm({ RegSwitch, isRegTeamsFull }: RegistrationFormProps) {
    const params = new URLSearchParams(window.location.search);
    const token = params.get('jwt_token') ?? undefined;
    //const _decodedToken: DecodedToken | null = token ? jwtDecode<DecodedToken>(token) : null;

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
            first_name: '',
            last_name: '',
            email: '',
            country: '',
            address: '',
            has_team: undefined,
            role: undefined,
            has_participated_in_hackathons: undefined,
            idea: '',
            challenge: '',
            motivation: '',
            best_describes: undefined,
        },
    });

    const onSubmit = (data: z.infer<typeof registrationSchema>) => {
        const payload: RegistrationInfo = {
            registration_info: { ...data },
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

    const isFormDisabled = isPending || isSubmitted;

    if (!RegSwitch || isRegTeamsFull) {
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
                        className="bg-white/10 backdrop-blur-lg w-full max-w-[90%] sm:max-w-[75%] px-6 sm:px-14 py-12 border border-white rounded-[2rem] shadow-[0_8px_30px_rgb(0,0,0,0.08)] mb-16"
                    >
                        {/* Personal Info Section */}
                        <div>
                            <p className="text-gray-800 text-base mb-2 mt-4 font-normal">Personal Info</p>
                            <hr className="mb-8 h-[2px] bg-red-300/60 border-0" />

                            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                                <InputComponent
                                    control={form.control}
                                    name="first_name"
                                    label="First Name"
                                    type="text"
                                    placeholder="John"
                                    labelClassName={labelStyles}
                                    inputClassName={inputStyles}
                                />
                                <InputComponent
                                    control={form.control}
                                    name="last_name"
                                    label="Last Name"
                                    type="text"
                                    placeholder="Doe"
                                    labelClassName={labelStyles}
                                    inputClassName={inputStyles}
                                />
                                <InputComponent
                                    control={form.control}
                                    name="email"
                                    label="Email"
                                    type="email"
                                    placeholder="john@doe.com"
                                    labelClassName={labelStyles}
                                    inputClassName={inputStyles}
                                />
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
                                <InputComponent
                                    control={form.control}
                                    name="country"
                                    label="Country"
                                    type="text"
                                    placeholder="Enter your country"
                                    labelClassName={labelStyles}
                                    inputClassName={inputStyles}
                                />
                                <InputComponent
                                    control={form.control}
                                    name="address"
                                    label="Address"
                                    type="text"
                                    placeholder="123 Main Street"
                                    labelClassName={labelStyles}
                                    inputClassName={inputStyles}
                                />
                            </div>
                        </div>

                        <div>
                            <p className="text-gray-800 text-base mt-12 mb-2 font-normal">Participation</p>
                            <hr className="mb-8 h-[2px] bg-red-300/60 border-0" />

                            <div className="flex flex-col gap-8">
                                <RadioComponent
                                    control={form.control}
                                    name="has_team"
                                    options={[
                                        { label: 'Yes', value: true },
                                        { label: 'No', value: false },
                                    ]}
                                    groupLabel="Do you have a team?"
                                    groupClassName={labelStyles}
                                    radioGroupClassName={radioGroupStyles}
                                />

                                <RadioComponent
                                    control={form.control}
                                    name="role"
                                    options={ROLE_OPTIONS}
                                    groupLabel="Which role will you take?"
                                    groupClassName={labelStyles}
                                    radioGroupClassName={radioGroupStyles}
                                />

                                <RadioComponent
                                    control={form.control}
                                    name="has_participated_in_hackathons"
                                    options={[
                                        { label: 'Yes', value: true },
                                        { label: 'No', value: false },
                                    ]}
                                    groupLabel="Have you participated in a hackathon before?"
                                    groupClassName={labelStyles}
                                    radioGroupClassName={radioGroupStyles}
                                />

                                <InputComponent
                                    control={form.control}
                                    name="idea"
                                    label="What is your idea?"
                                    type="text"
                                    placeholder="Type here..."
                                    labelClassName={labelStyles}
                                    inputClassName={inputStyles}
                                />

                                <InputComponent
                                    control={form.control}
                                    name="challenge"
                                    label="What challenge/problem does it address?"
                                    type="text"
                                    placeholder="Type here..."
                                    labelClassName={labelStyles}
                                    inputClassName={inputStyles}
                                />

                                <InputComponent
                                    control={form.control}
                                    name="motivation"
                                    label="Why do you want to take part in the hackathon?"
                                    type="text"
                                    placeholder="Type here..."
                                    labelClassName={labelStyles}
                                    inputClassName={inputStyles}
                                />

                                <RadioComponent
                                    control={form.control}
                                    name="best_describes"
                                    options={TRAIT_OPTIONS}
                                    groupLabel="Which describes you best?"
                                    groupClassName={labelStyles}
                                    radioGroupClassName={radioGroupStyles}
                                />
                            </div>
                        </div>

                        <div className="flex justify-start mt-8">
                            <Button
                                disabled={isFormDisabled}
                                type="submit"
                                className={`mt-4 px-8 py-2 text-sm text-gray-800 border-2 border-red-400 rounded-full bg-transparent hover:bg-red-400 transition-all duration-300 hover:text-white ${
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
                            <p className="text-sm text-red-600 mt-4">{error.message}</p>
                        )}

                        {isSubmitted && (
                            <div className="mt-4">
                                <Button
                                    type="button"
                                    onClick={onResendEmail}
                                    disabled={cooldown.isCoolingDown}
                                    className="px-6 py-2 text-sm text-gray-800 border border-gray-400 rounded-full bg-transparent hover:bg-gray-100 transition-all duration-300"
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
