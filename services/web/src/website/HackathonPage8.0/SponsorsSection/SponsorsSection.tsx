import { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';

import type { Sponsor as BackendSponsor } from '@/types/sponsors';
import { apiClient } from '@/services/apiClient';
import type { HackathonSponsorProps, SponsorRank } from './types';
import { VerticalBar } from '@/components/ui/verticalBar';
import type { CSSProperties } from 'react';

type Slot = { kind: 'sponsor'; sponsor: HackathonSponsorProps };

const RANK_CONFIG: Record<Extract<SponsorRank, 'Platinum' | 'Gold' | 'Silver'>, { label: string; color: string }> = {
    Platinum: { label: 'PLATINUM', color: '#19A0F0' },
    Gold: { label: 'GOLD', color: '#FFDE06' },
    Silver: { label: 'SILVER', color: '#8294A2' },
};

const SPONSORS_ENDPOINT = '/admin/sponsors';

// Pixel-matched layout constants (DESKTOP ARTBOARD)
const FRAME_W = 1520;
const FRAME_H = 1762;

const LEFT_ALIGN = 114;
const DIVIDER_W = 1206;

const PANEL_ML = 100;
const PANEL_W = 1256;
const PANEL_PL = 30;

const TILE = 230;
const COLS = 9;

const PANEL_BG =
    'linear-gradient(90deg, rgba(255, 253, 245, 1) 39%, rgba(255, 253, 245, 0.8) 74%, rgba(255, 253, 245, 0.6) 100%)';

const FLAMES_TOP = 20;

function buildSlots(sponsors: HackathonSponsorProps[]): Slot[] {
    return sponsors.map((sponsor) => ({ kind: 'sponsor', sponsor }));
}

function tierToRank(tier: string): SponsorRank {
    const t = tier.trim().toLowerCase();
    if (t === 'platinum') return 'Platinum';
    if (t === 'gold') return 'Gold';
    if (t === 'silver') return 'Silver';
    if (t === 'bronze') return 'Bronze';
    return 'Custom';
}

/** Map backend sponsor -> UI sponsor props */
function mapBackendSponsors(list: BackendSponsor[]): HackathonSponsorProps[] {
    return list.map((s) => ({
        name: s.name,
        rank: tierToRank(s.tier),
        logoSrc: s.logo_url,
        websiteLink: s.website_url,
    }));
}

/* ------------------------------- DESKTOP ARTBOARD ------------------------------- */

function SponsorTileFixed({ sponsor }: { sponsor: HackathonSponsorProps }) {
    return (
        <a
            href={sponsor.websiteLink}
            target="_blank"
            rel="noreferrer"
            className="block w-[230px] h-[230px] rounded-[16px] border border-[#6E6E6E] bg-transparent overflow-hidden"
        >
            <img
                src={sponsor.logoSrc}
                alt={sponsor.name}
                className="w-full rounded-[16px] h-full object-contain select-none"
                draggable={false}
            />
        </a>
    );
}

function RankSectionFixed({
    rank,
    sponsors,
}: {
    rank: Extract<SponsorRank, 'Platinum' | 'Gold' | 'Silver'>;
    sponsors: HackathonSponsorProps[];
}) {
    const { label, color } = RANK_CONFIG[rank];
    const slots = buildSlots(sponsors);

    return (
        <section className="relative">
            <div
                className="rounded-[22px]"
                style={{
                    width: PANEL_W,
                    marginLeft: PANEL_ML,
                    paddingTop: 28,
                    paddingBottom: 34,
                    paddingLeft: PANEL_PL,
                    paddingRight: 0,
                    background: PANEL_BG,
                }}
            >
                <div style={{ width: DIVIDER_W }}>
                    <div
                        className="font-oxanium uppercase tracking-[0.55em] text-[36px] leading-none"
                        style={{ color }}
                    >
                        {label}
                    </div>
                    <div className="h-[1px] bg-[#1D1B1A]" style={{ width: DIVIDER_W, marginTop: 29 }} />
                </div>

                {slots.length === 0 ? <div style={{ height: 280 }} /> : null}

                {slots.length > 0 ? (
                    <div
                        className="grid gap-x-[31px] gap-y-[24px]"
                        style={{
                            gridTemplateColumns: `repeat(${COLS}, ${TILE}px)`,
                            width: 1140,
                            marginTop: 50,
                        }}
                    >
                        {slots.map((slot) => (
                            <SponsorTileFixed key={slot.sponsor.name} sponsor={slot.sponsor} />
                        ))}
                    </div>
                ) : null}
            </div>
        </section>
    );
}

function SponsorsArtboard({
    sponsorsSwitch,
    sponsors,
}: {
    sponsorsSwitch: boolean;
    sponsors: HackathonSponsorProps[];
}) {
    const platinumSponsors = sponsors.filter((s) => s.rank === 'Platinum').sort((a, b) => a.name.localeCompare(b.name));
    const goldSponsors = sponsors.filter((s) => s.rank === 'Gold').sort((a, b) => a.name.localeCompare(b.name));
    const silverSponsors = sponsors.filter((s) => s.rank === 'Silver').sort((a, b) => a.name.localeCompare(b.name));

    return (
        <div
            className="relative rounded-[24px] bg-[#FFFDF5] shadow-[0_18px_60px_rgba(0,0,0,0.45)] overflow-hidden"
            style={{ width: FRAME_W, height: FRAME_H }}
        >
            {/* Flames scale perfectly because the whole artboard scales */}
            <img
                src="/flames.png"
                alt="Flame Background"
                className="absolute pointer-events-none select-none object-cover object-bottom"
                style={{
                    left: 0,
                    top: FLAMES_TOP,
                    width: '100%',
                    height: `calc(100% + ${FLAMES_TOP}px)`,
                }}
                draggable={false}
            />

            {/* Header */}
            <div className="absolute flex items-center gap-[14px]" style={{ left: LEFT_ALIGN, top: 160 }}>
                <img
                    src="/mockingjay-red.svg"
                    alt="Sponsors-Icon"
                    className="w-[52px] h-[42px] select-none"
                    draggable={false}
                />
                <h2 className="font-orbitron text-[40px] leading-[100%] text-[#DA2F2F] whitespace-nowrap">SPONSORS</h2>
            </div>

            <VerticalBar isRight={true} isBlack={true} />
            <VerticalBar isRight={false} isBlack={true} />

            {!sponsorsSwitch ? (
                <div className="absolute" style={{ left: LEFT_ALIGN, top: 260 }}>
                    <div className="text-[#D11B1B] tracking-[0.25em] text-[22px] select-none">
                        SPONSORS COMING SOON . . .
                    </div>
                </div>
            ) : (
                <div className="absolute left-0 right-0" style={{ top: 275 }}>
                    <RankSectionFixed rank="Platinum" sponsors={platinumSponsors} />
                    <div style={{ height: 45 }} />
                    <RankSectionFixed rank="Gold" sponsors={goldSponsors} />
                    <div style={{ height: 45 }} />
                    <RankSectionFixed rank="Silver" sponsors={silverSponsors} />
                </div>
            )}
        </div>
    );
}

/* ------------------------------- MOBILE LAYOUT ------------------------------- */

function SponsorTileFluid({ sponsor }: { sponsor: HackathonSponsorProps }) {
    return (
        <a
            href={sponsor.websiteLink}
            target="_blank"
            rel="noreferrer"
            className="w-full aspect-square rounded-[16px] border border-[#6E6E6E] bg-transparent overflow-hidden"
        >
            <img
                src={sponsor.logoSrc}
                alt={sponsor.name}
                className="w-full h-full rounded-[16px] object-contain select-none"
                draggable={false}
            />
        </a>
    );
}

function RankSectionMobile({
    rank,
    sponsors,
}: {
    rank: Extract<SponsorRank, 'Platinum' | 'Gold' | 'Silver'>;
    sponsors: HackathonSponsorProps[];
}) {
    const { label, color } = RANK_CONFIG[rank];
    const slots = buildSlots(sponsors);

    return (
        <div
            className="rounded-[22px]"
            style={{
                background: PANEL_BG,
                padding: 16,
            }}
        >
            <div className="font-oxanium uppercase tracking-[0.55em] text-[20px] leading-none" style={{ color }}>
                {label}
            </div>
            <div className="h-[1px] bg-[#1D1B1A]" style={{ width: '100%', marginTop: 18 }} />

            {slots.length === 0 ? <div style={{ height: 140 }} /> : null}

            {slots.length > 0 ? (
                <div
                    className="grid mt-[18px]"
                    style={{
                        gridTemplateColumns: 'repeat(auto-fill, minmax(160px, 230px))',
                        columnGap: 14,
                        rowGap: 14,
                        justifyContent: 'start',
                    }}
                >
                    {slots.map((slot) => (
                        <div key={slot.sponsor.name} style={{ maxWidth: 230 }}>
                            <SponsorTileFluid sponsor={slot.sponsor} />
                        </div>
                    ))}
                </div>
            ) : null}
        </div>
    );
}

function SponsorsMobile({ sponsorsSwitch, sponsors }: { sponsorsSwitch: boolean; sponsors: HackathonSponsorProps[] }) {
    const platinumSponsors = sponsors.filter((s) => s.rank === 'Platinum').sort((a, b) => a.name.localeCompare(b.name));
    const goldSponsors = sponsors.filter((s) => s.rank === 'Gold').sort((a, b) => a.name.localeCompare(b.name));
    const silverSponsors = sponsors.filter((s) => s.rank === 'Silver').sort((a, b) => a.name.localeCompare(b.name));

    return (
        <div className="relative rounded-[24px] bg-[#FFFDF5] shadow-[0_18px_60px_rgba(0,0,0,0.45)] overflow-hidden w-full">
            <img
                src="/flames.png"
                alt="Flame Background"
                className="absolute pointer-events-none select-none object-cover object-bottom"
                style={{
                    left: 0,
                    top: 0,
                    width: '100%',
                    height: '100%',
                }}
                draggable={false}
            />

            {/* mobile header */}
            <div className="relative z-10 px-[16px] pt-[26px] pb-[18px]">
                <div className="flex items-center gap-[12px]">
                    <img
                        src="/mockingjay-red.svg"
                        alt="Sponsors-Icon"
                        className="w-[44px] h-[36px] select-none"
                        draggable={false}
                    />
                    <h2 className="font-orbitron text-[28px] leading-[100%] text-[#DA2F2F] whitespace-nowrap">
                        SPONSORS
                    </h2>
                </div>

                {!sponsorsSwitch ? (
                    <div className="mt-[22px] text-[#D11B1B] tracking-[0.25em] text-[16px] select-none">
                        SPONSORS COMING SOON . . .
                    </div>
                ) : (
                    <div className="mt-[22px] flex flex-col gap-[16px]">
                        <RankSectionMobile rank="Platinum" sponsors={platinumSponsors} />
                        <RankSectionMobile rank="Gold" sponsors={goldSponsors} />
                        <RankSectionMobile rank="Silver" sponsors={silverSponsors} />
                    </div>
                )}
            </div>
        </div>
    );
}

/* ---------------------------------- EXPORT ---------------------------------- */

export const SponsorsSection = ({ sponsorsSwitch = true }: { sponsorsSwitch?: boolean }) => {
    // Fetch from backend (same approach as Admin SponsorsPage)
    const { data, isError } = useQuery({
        queryKey: ['public-sponsors'],
        queryFn: () => apiClient.get<{ sponsors: BackendSponsor[] }>(SPONSORS_ENDPOINT),
        select: (res) => res.sponsors,
    });

    const sponsorsFromBackend = useMemo(() => mapBackendSponsors(data ?? []), [data]);

    // If backend fails, we still render (with placeholders)
    const effectiveSponsors = isError ? [] : sponsorsFromBackend;

    const scaledStyle: CSSProperties & { ['--s']: string } = {
        width: '100%',
        maxWidth: FRAME_W,
        ['--s']: `min(1, calc(100% / ${FRAME_W}))`,
        height: `calc(${FRAME_H}px * var(--s))`,
    };

    return (
        <div className="w-full bg-black flex justify-center">
            <div className="w-full">
                {/* Mobile */}
                <div className="block sm:hidden max-w-[560px] mx-auto">
                    <SponsorsMobile sponsorsSwitch={sponsorsSwitch} sponsors={effectiveSponsors} />
                </div>

                {/* Tablet/Laptop/Desktop */}
                <div className="hidden sm:block mx-auto" style={scaledStyle}>
                    <div
                        style={{
                            width: FRAME_W,
                            height: FRAME_H,
                            transform: 'scale(var(--s))',
                            transformOrigin: 'top left',
                        }}
                    >
                        <SponsorsArtboard sponsorsSwitch={sponsorsSwitch} sponsors={effectiveSponsors} />
                    </div>
                </div>
            </div>
        </div>
    );
};
