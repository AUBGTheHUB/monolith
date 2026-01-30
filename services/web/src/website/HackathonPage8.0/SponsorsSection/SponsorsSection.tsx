// services/web/src/website/HackathonPage8.0/SponsorsSection/SponsorsSection.tsx
import { Sponsors } from './sponsors';
import type { HackathonSponsorProps, SponsorRank } from './types';
import { VerticalBar } from '@/components/ui/verticalBar';
import type { CSSProperties } from 'react';

type Slot = { kind: 'sponsor'; sponsor: HackathonSponsorProps } | { kind: 'placeholder'; key: string };

const RANK_CONFIG: Record<Extract<SponsorRank, 'Platinum' | 'Gold' | 'Silver'>, { label: string; color: string }> = {
    Platinum: { label: 'PLATINUM', color: '#19A0F0' },
    Gold: { label: 'GOLD', color: '#FFDE06' },
    Silver: { label: 'SILVER', color: '#8294A2' },
};

// Pixel-matched layout constants (DESKTOP ARTBOARD)
const FRAME_W = 1520;
const FRAME_H = 1762;

const LEFT_ALIGN = 114;
const DIVIDER_W = 1206;

const PANEL_ML = 100;
const PANEL_W = 1256;
const PANEL_PL = 30;

const TILE = 103;
const COLS = 9;

const PANEL_BG =
    'linear-gradient(90deg, rgba(255, 253, 245, 1) 39%, rgba(255, 253, 245, 0.8) 74%, rgba(255, 253, 245, 0.6) 100%)';

const FLAMES_TOP = 20;

function buildSlots(sponsors: HackathonSponsorProps[], minSlots = 10): Slot[] {
    const out: Slot[] = sponsors.map((sponsor) => ({ kind: 'sponsor', sponsor }));
    for (let i = out.length; i < minSlots; i += 1) out.push({ kind: 'placeholder', key: `ph-${i}` });
    return out;
}

/* ------------------------------- DESKTOP ARTBOARD ------------------------------- */

function SponsorTileFixed({ sponsor }: { sponsor: HackathonSponsorProps }) {
    return (
        <a
            href={sponsor.websiteLink}
            target="_blank"
            rel="noreferrer"
            className="block w-[100px] h-[100px] rounded-[16px] border border-[#6E6E6E] bg-transparent overflow-hidden"
        >
            <div className="w-full h-full p-[18px] flex items-center justify-center">
                <img
                    src={sponsor.logoSrc}
                    alt={sponsor.name}
                    className="w-full h-full object-contain select-none"
                    draggable={false}
                />
            </div>
        </a>
    );
}

function PlaceholderTileFixed() {
    return (
        <div className="w-[100px] h-[100px] rounded-[16px] border border-[#6E6E6E] bg-transparent relative overflow-hidden">
            <span className="absolute inset-0 flex items-center justify-center text-[#BFC6CC] opacity-35 text-[16px] tracking-[0.14em] select-none">
                EVIDEN
            </span>
        </div>
    );
}

function RankSectionFixed({
    rank,
    sponsors,
    minSlots = 10,
}: {
    rank: Extract<SponsorRank, 'Platinum' | 'Gold' | 'Silver'>;
    sponsors: HackathonSponsorProps[];
    minSlots?: number;
}) {
    const { label, color } = RANK_CONFIG[rank];
    const slots = buildSlots(sponsors, minSlots);

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

                <div
                    className="grid gap-x-[31px] gap-y-[24px]"
                    style={{
                        gridTemplateColumns: `repeat(${COLS}, ${TILE}px)`,
                        width: 1140,
                        marginTop: 50,
                    }}
                >
                    {slots.map((slot, idx) =>
                        slot.kind === 'sponsor' ? (
                            <SponsorTileFixed key={slot.sponsor.name} sponsor={slot.sponsor} />
                        ) : (
                            <PlaceholderTileFixed key={`${slot.key}-${idx}`} />
                        ),
                    )}
                </div>
            </div>
        </section>
    );
}

function SponsorsArtboard({ sponsorsSwitch }: { sponsorsSwitch: boolean }) {
    const platinumSponsors = Sponsors.filter((s) => s.rank === 'Platinum').sort((a, b) => a.name.localeCompare(b.name));
    const goldSponsors = Sponsors.filter((s) => s.rank === 'Gold').sort((a, b) => a.name.localeCompare(b.name));
    const silverSponsors = Sponsors.filter((s) => s.rank === 'Silver').sort((a, b) => a.name.localeCompare(b.name));

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
                    <RankSectionFixed rank="Platinum" sponsors={platinumSponsors} minSlots={10} />
                    <div style={{ height: 45 }} />
                    <RankSectionFixed rank="Gold" sponsors={goldSponsors} minSlots={10} />
                    <div style={{ height: 45 }} />
                    <RankSectionFixed rank="Silver" sponsors={silverSponsors} minSlots={10} />
                </div>
            )}

            {/* Corner flame stays positioned relative to artboard */}
            <img
                src="/hackathon8/sponsors/flame-corner.png"
                alt=""
                className="absolute pointer-events-none select-none"
                style={{ right: -140, bottom: 40, width: 520 }}
                draggable={false}
            />
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
            <div className="w-full h-full p-[12px] flex items-center justify-center">
                <img
                    src={sponsor.logoSrc}
                    alt={sponsor.name}
                    className="w-full h-full object-contain select-none"
                    draggable={false}
                />
            </div>
        </a>
    );
}

function PlaceholderTileFluid() {
    return (
        <div className="w-full aspect-square rounded-[16px] border border-[#6E6E6E] bg-transparent relative overflow-hidden">
            <span className="absolute inset-0 flex items-center justify-center text-[#BFC6CC] opacity-35 text-[14px] tracking-[0.14em] select-none">
                EVIDEN
            </span>
        </div>
    );
}

function RankSectionMobile({
    rank,
    sponsors,
    minSlots = 10,
}: {
    rank: Extract<SponsorRank, 'Platinum' | 'Gold' | 'Silver'>;
    sponsors: HackathonSponsorProps[];
    minSlots?: number;
}) {
    const { label, color } = RANK_CONFIG[rank];
    const slots = buildSlots(sponsors, minSlots);

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

            <div
                className="grid mt-[18px]"
                style={{
                    gridTemplateColumns: 'repeat(auto-fill, minmax(76px, 100px))',
                    columnGap: 14,
                    rowGap: 14,
                    justifyContent: 'start',
                }}
            >
                {slots.map((slot, idx) =>
                    slot.kind === 'sponsor' ? (
                        <div key={slot.sponsor.name} style={{ maxWidth: 100 }}>
                            <SponsorTileFluid sponsor={slot.sponsor} />
                        </div>
                    ) : (
                        <div key={`${slot.key}-${idx}`} style={{ maxWidth: 100 }}>
                            <PlaceholderTileFluid />
                        </div>
                    ),
                )}
            </div>
        </div>
    );
}

function SponsorsMobile({ sponsorsSwitch }: { sponsorsSwitch: boolean }) {
    const platinumSponsors = Sponsors.filter((s) => s.rank === 'Platinum').sort((a, b) => a.name.localeCompare(b.name));
    const goldSponsors = Sponsors.filter((s) => s.rank === 'Gold').sort((a, b) => a.name.localeCompare(b.name));
    const silverSponsors = Sponsors.filter((s) => s.rank === 'Silver').sort((a, b) => a.name.localeCompare(b.name));

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
                        <RankSectionMobile rank="Platinum" sponsors={platinumSponsors} minSlots={10} />
                        <RankSectionMobile rank="Gold" sponsors={goldSponsors} minSlots={10} />
                        <RankSectionMobile rank="Silver" sponsors={silverSponsors} minSlots={10} />
                    </div>
                )}
            </div>
        </div>
    );
}

/* ---------------------------------- EXPORT ---------------------------------- */

export const SponsorsSection = ({ sponsorsSwitch = true }: { sponsorsSwitch?: boolean }) => {
    const scaledStyle: CSSProperties & { ['--s']: string } = {
        width: '100%',
        maxWidth: FRAME_W,
        ['--s']: `min(1, calc(100% / ${FRAME_W}))`,
        height: `calc(${FRAME_H}px * var(--s))`,
    };
    return (
        <div className="w-full bg-black flex justify-center">
            <div className="w-full">
                {/* Mobile: reflow layout */}
                <div className="block sm:hidden max-w-[560px] mx-auto">
                    <SponsorsMobile sponsorsSwitch={sponsorsSwitch} />
                </div>

                {/* Tablet/Laptop/Desktop: pixel-perfect artboard that scales down proportionally */}
                <div className="hidden sm:block mx-auto" style={scaledStyle}>
                    <div
                        style={{
                            width: FRAME_W,
                            height: FRAME_H,
                            transform: 'scale(var(--s))',
                            transformOrigin: 'top left',
                        }}
                    >
                        <SponsorsArtboard sponsorsSwitch={sponsorsSwitch} />
                    </div>
                </div>
            </div>
        </div>
    );
};
