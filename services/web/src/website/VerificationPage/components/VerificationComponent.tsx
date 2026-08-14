import { API_URL } from '@/constants';
import { useQuery } from '@tanstack/react-query';
import { BadgeCheck, CircleAlert, Link2Off, Loader2 } from 'lucide-react';
import { useEffect, useMemo, useState } from 'react';
import flameBR from '../../RegistrationFormPage/RegistrationForm/images/flame_BR.png';
import flameTL from '../../RegistrationFormPage/RegistrationForm/images/flame_TL.png';

export async function verifyToken(token: string) {
    const params = new URLSearchParams();
    params.set('jwt_token', token);

    let response;
    try {
        response = await fetch(`${API_URL}/hackathon/participants/verify?${params.toString()}`, { method: 'PATCH' });
    } catch {
        throw new Error('Verification failed, try refreshing the page or contact us.');
    }
    const data = await response.json();
    if (!response.ok) {
        throw new Error((data && data.error) || 'Verification failed, try refreshing the page or contact us.');
    }
    return data;
}

export const VerificationComponent = () => {
    const [fadeIn, setFadeIn] = useState(false);

    useEffect(() => {
        const timer = setTimeout(() => setFadeIn(true), 80);
        return () => clearTimeout(timer);
    }, []);

    const token = useMemo(() => {
        const params = new URLSearchParams(window.location.search);
        return params.get('jwt_token');
    }, []);

    const { isLoading, isError, error } = useQuery({
        queryKey: ['verifyToken', token],
        queryFn: () => verifyToken(token as string),
        enabled: !!token,
        retry: 1,
        refetchOnWindowFocus: false,
    });

    let title = 'Verification successful!';
    let content = 'Please check your email for next steps.';
    let icon = <BadgeCheck className="h-8 w-8" />;
    let iconClass = 'bg-emerald-50 text-emerald-700 border-emerald-200';

    if (isLoading) {
        title = 'Verifying your access...';
        content = 'Hold tight while we confirm your registration token.';
        icon = <Loader2 className="h-8 w-8 animate-spin" />;
        iconClass = 'bg-amber-50 text-amber-700 border-amber-200';
    } else if (isError) {
        title = 'Verification failed.';
        content = `Error: ${(error as Error).message}`;
        icon = <CircleAlert className="h-8 w-8" />;
        iconClass = 'bg-red-50 text-red-700 border-red-200';
    } else if (!token) {
        title = 'Link is invalid.';
        content = 'The verification link is missing or malformed. Open the latest email and try again.';
        icon = <Link2Off className="h-8 w-8" />;
        iconClass = 'bg-gray-100 text-gray-600 border-gray-300';
    }

    return (
        <div
            className={`w-full flex flex-col items-center overflow-hidden font-mont bg-[#fafafa] relative text-gray-800 min-h-screen transition-opacity duration-700 ${fadeIn ? 'opacity-100' : 'opacity-0'}`}
        >
            <img
                src={flameTL}
                alt=""
                className="absolute top-0 left-0 w-[650px] opacity-90 z-0 pointer-events-none mix-blend-multiply"
            />
            <img
                src={flameBR}
                alt=""
                className="absolute bottom-0 right-0 w-[650px] opacity-90 z-0 pointer-events-none mix-blend-multiply"
            />

            <div className="w-11/12 sm:w-4/5 flex justify-center mt-24 mb-8 z-10">
                <p className="text-gray-900 tracking-[0.4em] text-3xl sm:text-4xl font-medium uppercase text-center">
                    VERIFICATION
                </p>
            </div>

            <div className="w-full flex justify-center z-10 px-4 pb-16">
                <div className="w-full max-w-3xl bg-white/75 backdrop-blur-md rounded-[2rem] border border-white shadow-[0_8px_30px_rgb(0,0,0,0.08)] px-6 sm:px-12 py-10 sm:py-12">
                    <div className="flex flex-col sm:flex-row sm:items-start items-center gap-5 sm:gap-6">
                        <div
                            className={`h-16 w-16 rounded-full border flex items-center justify-center shrink-0 ${iconClass}`}
                        >
                            {icon}
                        </div>

                        <div className="text-center sm:text-left">
                            <p className="text-2xl sm:text-3xl text-gray-900 font-medium">{title}</p>
                            <p className="mt-2 text-gray-600 text-base sm:text-lg">{content}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
