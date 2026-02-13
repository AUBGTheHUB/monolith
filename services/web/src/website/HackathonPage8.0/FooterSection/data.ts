import { FooterColumn } from './types';

export const footerData: FooterColumn[] = [
    {
        id: 1,
        title: 'Address',
        items: [
            { label: 'AUBG' },
            { label: 'Blagoevgrad, Bulgaria' },
        ],
    },
    {
        id: 2,
        title: 'Links',
        items: [
            { label: 'Home', href: '#' },
            { label: 'About us', href: '#' },
            { label: 'Events', href: '#' },
            { label: 'The team', href: '#' },
            { label: 'Hack Aubg', href: '#' },
        ],
    },
    {
        id: 3,
        title: 'Socials',
        items: [
            { label: 'Instagram', href: '#' },
            { label: 'Youtube', href: '#' },
            { label: 'Facebook', href: '#' },
        ],
    },
    {
        id: 4,
        title: 'Contact',
        items: [
            { label: 'thehub@aubg.edu', href: 'mailto:thehub@aubg.edu' },
        ],
    },
];