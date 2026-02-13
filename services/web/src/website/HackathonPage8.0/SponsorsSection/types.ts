// services/web/src/website/HackathonPage8.0/SponsorsSection/types.ts
export type SponsorRank = 'Platinum' | 'Gold' | 'Silver';

export interface HackathonSponsorProps {
    rank: SponsorRank;
    name: string;
    logoSrc: string;
    websiteLink: string;
}
