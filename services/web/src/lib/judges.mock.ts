export type Judge = {
    id: string;
    name: string;
    companyName: string;
    imageUrl: string;
};

export const MOCK_JUDGES: Judge[] = [
    {
        id: '1',
        name: 'Carmen Struck',
        companyName: 'TechCorp AI',
        imageUrl: '/carmen_struck_round.webp',
    },
    {
        id: '2',
        name: 'Daniel Lydianov',
        companyName: 'Venture Capital Partners',
        imageUrl: '/daniel_lydianov_round.webp',
    },
    {
        id: '3',
        name: 'Anton Polimenov',
        companyName: 'CloudSystems Inc',
        imageUrl: '/anton_polimenov_round.webp',
    },
];
