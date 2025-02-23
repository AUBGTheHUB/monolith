import { API_URL } from '@/constants';
import { Navigation } from '@/website/HackathonPage/Navigation/Navigation';
import { useQuery } from '@tanstack/react-query';

export async function verifyToken(token: string) {
    const params = new URLSearchParams();
    params.set('jwt_token', token);

    let response;
    try {
        response = await fetch(`${API_URL}/hackathon/participants/verify?${params.toString()}`, { method: 'PATCH' });
    } catch {
        throw new Error('Verification failed, try refreshing the page or contact us.');
    }
    console.log(response);
    const data = await response.json();
    console.log(data);
    if (!response.ok) {
        console.log(data.error);
        throw new Error((data && data.error) || 'Verification failed, try refreshing the page or contact us.');
    }
    return data;
}

export const VerificationComponent = () => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get('jwt_token');
    const { isLoading, isError, error } = useQuery({
        queryKey: ['verifyToken', token],
        queryFn: () => verifyToken(token as string),
        enabled: !!token,
        retry: 1,
        refetchOnWindowFocus: false,
    });

    let content;

    if (isLoading) {
        content = 'Loading...';
    } else if (isError) {
        content = `Error: ${(error as Error).message}`;
    } else if (!token) {
        content = 'Link is invalid';
    } else {
        content = 'Verification successful';
    }

    return (
        <div style={{ backgroundImage: 'url("/verifyPage/background.png")' }} className="min-h-[100vh]">
            <Navigation />
            <div className="  bg-center flex items-center h-[75vh] sm:h-[85vh]">
                <div className="text-white w-full flex h-[200px] justify-center">
                    <div className="bg-[#000b13] w-4/5 h-full rounded-md border border-[#202d38] flex justify-center items-center font-mont text-2xl">
                        <p className="text-center p-5">{content}</p>
                    </div>
                </div>
            </div>
        </div>
    );
};
