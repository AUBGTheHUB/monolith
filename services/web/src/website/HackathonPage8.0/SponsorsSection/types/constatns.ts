export const SPONSOR_RANKS = ['PLATINUM', 'GOLD', 'SILVER', 'BRONZE', 'CUSTOM'] as const;
export type SponsorRank = (typeof SPONSOR_RANKS)[number];

export interface Sponsor {
    id: string;
    rank: SponsorRank;
    name: string;
    logoSrc: string;
    websiteLink: string;
}

export type BackendSponsor = {
    id: string;
    name: string;
    tier: string;
    logo_url: string;
    website_url: string;
};

export const SPONSOR_RANK_META: Record<SponsorRank, { label: string; color: string; hoverShadowClass: string }> = {
    PLATINUM: { label: 'PLATINUM', color: '#19A0F0', hoverShadowClass: 'hover:shadow-[#19A0F0]' },
    GOLD: { label: 'GOLD', color: '#FFDE06', hoverShadowClass: 'hover:shadow-[#FFDE06]' },
    SILVER: { label: 'SILVER', color: '#92B1C9', hoverShadowClass: 'hover:shadow-[#92B1C9]' },
    BRONZE: { label: 'BRONZE', color: '#CD7F32', hoverShadowClass: 'hover:shadow-[#CD7F32]' },
    CUSTOM: { label: 'CUSTOM', color: '#505050', hoverShadowClass: 'hover:shadow-[#505050]' },
};
