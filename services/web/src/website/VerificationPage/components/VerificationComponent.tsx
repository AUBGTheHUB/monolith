import { API_URL } from '@/constants';
import { Navigation } from '@/website/HackathonPage/Navigation/Navigation';
import { useQuery } from '@tanstack/react-query';

export async function verifyToken(token: string) {
    console.log('From env', API_URL);
    const params = new URLSearchParams();
    params.set('jwt_token', token);

    const response = await fetch(`${API_URL}/hackathon/participants/verify?${params.toString()}`, { method: 'PATCH' });
    const data = await response.json();
    console.log('Parsed response:', data);
    if (!response.ok) {
        throw new Error((data && data.error) || 'Verification failed, try refreshing the page or contact us');
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
    });

    let content;
    if (isLoading) {
        content = <p className="font-mont">Loading...</p>;
    } else if (isError) {
        console.log(error);
        content = <p>Error: {(error as Error).message}</p>;
    } else {
        content = <p>Verification successful</p>;
    }

    return (
        <div style={{ backgroundImage: 'url("/verifyPage/background.png")' }} className="min-h-[100vh]">
            <Navigation />
            <div className="  bg-center flex items-center h-[75vh] sm:h-[85vh]">
                <div className="text-white w-full flex h-[200px] justify-center">
                    <div className="bg-[#000b13] w-4/5 h-full rounded-md border border-[#202d38] flex justify-center items-center font-mont">
                        {content}
                    </div>
                </div>
            </div>
        </div>
    );
};
