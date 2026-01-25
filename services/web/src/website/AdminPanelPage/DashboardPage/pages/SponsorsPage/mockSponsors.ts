// You might need to define this interface in your @/types/sponsor file
export interface Sponsor {
    id: string;
    name: string;
    tier: string; // This represents the "Badge" (e.g., Gold, Silver)
    logoUrl: string;
    websiteUrl: string;
    careersUrl?: string;
}

export const MOCK_SPONSORS: Sponsor[] = [
    {
        id: '1',
        name: 'TechGiant',
        tier: 'Diamond',
        logoUrl: '/logos/techgiant.webp',
        websiteUrl: 'https://techgiant.com',
        careersUrl: 'https://techgiant.com/careers',
    },
    {
        id: '2',
        name: 'DevSolutions',
        tier: 'Gold',
        logoUrl: '/logos/devsolutions.webp',
        websiteUrl: 'https://devsolutions.io',
        careersUrl: 'https://devsolutions.io/jobs',
    },
    {
        id: '3',
        name: 'StartUp Inc',
        tier: 'Silver',
        logoUrl: '/logos/startup.webp',
        websiteUrl: 'https://startup.inc',
    },
];