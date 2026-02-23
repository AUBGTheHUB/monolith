import { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/services/apiClient';
import {
    SPONSOR_RANKS,
    type Sponsor,
    type SponsorRank,
    type BackendSponsor,
    type FeatureSwitch,
    SPONSORS_SWITCH_NAME,
} from './types/constatns';
import { SponsorRankSection } from './components/SponsorRank';

const RANK_SET = new Set<string>(SPONSOR_RANKS);

function tierToRank(tier: string): SponsorRank {
    const normalized = (tier ?? '').trim().toUpperCase();
    return (RANK_SET.has(normalized) ? normalized : 'CUSTOM') as SponsorRank;
}

function groupAndSortSponsors(sponsors: Sponsor[]): Record<SponsorRank, Sponsor[]> {
    const grouped = SPONSOR_RANKS.reduce(
        (acc, rank) => {
            acc[rank] = [];
            return acc;
        },
        {} as Record<SponsorRank, Sponsor[]>,
    );

    for (const s of sponsors) grouped[s.rank].push(s);
    for (const rank of SPONSOR_RANKS) grouped[rank].sort((a, b) => a.name.localeCompare(b.name));

    return grouped;
}

function SponsorsComingSoon() {
    return (
        <section className="relative border w-full overflow-hidden bg-[rgba(255,253,245,1)]">
            <img
                src="/flames.png"
                alt="Flame Background"
                className="absolute inset-0 w-full h-full pointer-events-none select-none object-cover object-[50%_70%] transform-gpu
                    scale-[1.45] sm:scale-[1.25] lg:scale-[1.18] xl:scale-100"
                draggable={false}
            />
            <div className="relative text-[#233340] sm:w-[80%] mx-6 sm:mx-auto py-10 sm:py-20">
                <div className="text-3xl sm:text-4xl flex items-center gap-4">
                    <img
                        src="/mockingjay-red.svg"
                        alt="Sponsors-Icon"
                        className="w-[44px] h-[36px] sm:w-[52px] sm:h-[42px] select-none"
                        draggable={false}
                    />
                    <h2 className="tracking-[0.2em]">SPONSORS COMING SOON . . .</h2>
                </div>
            </div>
        </section>
    );
}

export function SponsorsSection() {
    const {
        data: sponsorsSwitch = false,
        isLoading: isSwitchLoading,
        isError: isSwitchError,
    } = useQuery({
        queryKey: ['feature-switches', SPONSORS_SWITCH_NAME],
        queryFn: () => apiClient.get<{ features: FeatureSwitch[] }>('/feature-switches'),
        select: (res) => res.features.find((f) => f.name === SPONSORS_SWITCH_NAME)?.state ?? false,
        staleTime: 0,
        refetchOnWindowFocus: true,
    });

    const {
        data: sponsors = [],
        isLoading: isSponsorsLoading,
        isError: isSponsorsError,
    } = useQuery({
        queryKey: ['hackathon', 'sponsors'],
        enabled: sponsorsSwitch === true,
        queryFn: () => apiClient.get<{ sponsors: BackendSponsor[] }>('/admin/sponsors'),
        select: (res): Sponsor[] =>
            res.sponsors.map((s) => ({
                id: s.id,
                name: s.name,
                rank: tierToRank(s.tier),
                logoSrc: s.logo_url,
                websiteLink: s.website_url,
            })),
    });

    const grouped = useMemo(() => groupAndSortSponsors(sponsors), [sponsors]);

    if (isSwitchLoading || isSwitchError || !sponsorsSwitch) {
        return <SponsorsComingSoon />;
    }

    return (
        <section className="relative w-full overflow-hidden bg-[rgba(255,253,245,1)]">
            <img
                src="/flames.png"
                alt="Flame Background"
                className="absolute inset-0 w-full h-full pointer-events-none select-none object-cover object-[50%_70%] transform-gpu
                 scale-[1.45] sm:scale-[1.25] lg:scale-[1.18] xl:scale-100"
                draggable={false}
            />

            <div className="relative text-[#233340] sm:w-[75%] mx-6 sm:mx-auto py-10 sm:py-20">
                <div className="flex flex-col gap-2 sm:gap-3">
                    <div className="flex items-center gap-4">
                        <img
                            src="/mockingjay-red.svg"
                            alt="Sponsors-Icon"
                            className="w-[2.75rem] h-[2.25rem] sm:w-[3.25rem] sm:h-[2.625rem] select-none"
                            draggable={false}
                        />
                        <h2 className="font-orbitron text-3xl sm:text-4xl leading-[100%] text-[#DA2F2F] whitespace-nowrap">
                            SPONSORS
                        </h2>
                    </div>

                    {isSponsorsLoading ? (
                        <div className="flex items-center gap-3 pl-[3.25rem] sm:pl-[3.75rem]">
                            <span className="h-4 w-4 animate-spin rounded-full border-2 border-[#233340]/30 border-t-[#233340]" />
                            <span className="text-base sm:text-xl text-[#233340]/70 tracking-wide">
                                Loading sponsors…
                            </span>
                        </div>
                    ) : null}

                    {isSponsorsError ? (
                        <div className="pl-[3.25rem] sm:pl-[3.75rem] text-base sm:text-xl text-[#233340]/70 tracking-wide">
                            Failed to load sponsors.
                        </div>
                    ) : null}
                </div>

                {SPONSOR_RANKS.map((rank) => (
                    <SponsorRankSection key={rank} rank={rank} sponsors={grouped[rank]} />
                ))}
            </div>
        </section>
    );
}
