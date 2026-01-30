import type { Judge } from '../../../../types/judge.ts';

export const MOCK_JUDGES: Judge[] = [
    {
        id: '1',
        name: 'Carmen Struck',
        companyName: 'TechCorp AI',
        imageUrl: '/carmen_struck_round.webp',
        position: 'Chief Technology Officer',
        linkedinURL: 'https://linkedin.com/in/carmenstruck',
    },
    {
        id: '2',
        name: 'Daniel Lydianov',
        companyName: 'Venture Capital Partners',
        imageUrl: '/daniel_lydianov_round.webp',
        position: 'Venture Capitalist',
        linkedinURL: 'https://linkedin.com/in/daniellydianov',
    },
    {
        id: '3',
        name: 'Anton Polimenov',
        companyName: 'CloudSystems Inc',
        imageUrl: '/anton_polimenov_round.webp',
        position: 'Head of Cloud Infrastructure',
        linkedinURL: 'https://linkedin.com/in/antonpolimenov',
    },
];
