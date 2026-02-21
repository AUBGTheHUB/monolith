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
            { label: 'Mission', href: '#mission' },
            { label: 'Schedule', href: '#schedule' },
            { label: 'Hackathon 7.0', href: '#hackathon7.0' },
            { label: 'Grading Criteria', href: '#grading-criteria' },
            { label: 'Awards', href: '#awards' },
            { label: 'FAQ', href: '#faq' },
        ],
    },
    {
        id: 3,
        title: 'Socials',
        items: [
            { label: 'Instagram', href: 'https://www.instagram.com/thehubaubg/' },
            { label: 'Youtube', href: 'https://www.youtube.com/@thehubaubg8522' },
            { label: 'Facebook', href: 'https://www.facebook.com/TheHubAUBG' },
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