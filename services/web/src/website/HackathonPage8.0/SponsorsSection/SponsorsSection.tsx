// services/web/src/website/HackathonPage8.0/SponsorsSection/SponsorsSection.tsx
import { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';

import type { Sponsor as BackendSponsor } from '@/types/sponsors';
import { apiClient } from '@/services/apiClient';
import type { HackathonSponsorProps, SponsorRank } from './types';
import { SponsorsCard } from './SponsorsCard';

const SPONSORS_ENDPOINT = '/admin/sponsors';

function tierToRank(tier: string): SponsorRank | null {
    const t = tier.trim().toLowerCase();
    if (t === 'platinum') return 'Platinum';
    if (t === 'gold') return 'Gold';
    if (t === 'silver') return 'Silver';
    return null;
}

function mapBackendSponsors(list: BackendSponsor[]): HackathonSponsorProps[] {
    return list
        .map((s) => {
            const rank = tierToRank(s.tier);
            if (!rank) return null;
            return {
                name: s.name,
                rank,
                logoSrc: s.logo_url,
                websiteLink: s.website_url,
            };
        })
        .filter((x): x is HackathonSponsorProps => x !== null);
}

function groupSponsors(sponsors: HackathonSponsorProps[]): Record<SponsorRank, HackathonSponsorProps[]> {
    const groups: Record<SponsorRank, HackathonSponsorProps[]> = {
        Platinum: [],
        Gold: [],
        Silver: [],
    };

    for (const s of sponsors) groups[s.rank].push(s);

    (Object.keys(groups) as SponsorRank[]).forEach((rank) => {
        groups[rank].sort((a, b) => a.name.localeCompare(b.name));
    });

    return groups;
}

export const SponsorsSection = ({ sponsorsSwitch = true }: { sponsorsSwitch?: boolean }) => {
    const { data, isError } = useQuery({
        queryKey: ['public-sponsors'],
        queryFn: () => apiClient.get<{ sponsors: BackendSponsor[] }>(SPONSORS_ENDPOINT),
        select: (res) => res.sponsors,
    });

    const sponsors = useMemo(() => (isError ? [] : mapBackendSponsors(data ?? [])), [data, isError]);
    const grouped = useMemo(() => groupSponsors(sponsors), [sponsors]);

    return (
        <div className="w-full bg-black">
            <div className="w-full">
                <SponsorsCard sponsorsSwitch={sponsorsSwitch} grouped={grouped} />
            </div>
        </div>
    );
};
