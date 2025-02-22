import { Fragment } from 'react/jsx-runtime';
import { useEffect, useRef } from 'react';
import { API_URL } from '@/constants';

export async function useFetchFeatureSwitches(token: string) {
    console.log('From env', API_URL);

    const params = new URLSearchParams();
    params.set('jwt_token', token);

    try {
        const response = await fetch(`${API_URL}/hackathon/participants/verify?${params.toString()}`, {
            method: 'PATCH',
        });

        console.log(response);
    } catch (error) {
        console.error('Error fetching feature switches:', error);
    }
}

export const VerificationComponent = () => {
    const hasFetched = useRef(false);

    useEffect(() => {
        const params = new URLSearchParams(window.location.search);
        const token = params.get('jwt_token');
        if (token) {
            useFetchFeatureSwitches(token);
            hasFetched.current = true;
        }
    }, []);

    return <Fragment></Fragment>;
};
