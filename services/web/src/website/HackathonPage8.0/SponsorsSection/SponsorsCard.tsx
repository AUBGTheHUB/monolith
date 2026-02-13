// services/web/src/website/HackathonPage8.0/SponsorsSection/SponsorsCard.tsx
import type { HackathonSponsorProps, SponsorRank } from './types';
import { VerticalBar } from '@/components/ui/verticalBar';

const PANEL_BG =
    'linear-gradient(90deg, rgba(255, 253, 245, 1) 39%, rgba(255, 253, 245, 0.8) 74%, rgba(255, 253, 245, 0.6) 100%)';

type RankMeta = {
    label: string;
    color: string;
    /** show panel even if there are 0 sponsors */
    alwaysShow: boolean;
};

const RANK_META: Record<SponsorRank, RankMeta> = {
    Platinum: { label: 'PLATINUM', color: '#19A0F0', alwaysShow: true },
    Gold: { label: 'GOLD', color: '#FFDE06', alwaysShow: true },
    Silver: { label: 'SILVER', color: '#8294A2', alwaysShow: true },
};

const PRIMARY_RANKS: SponsorRank[] = ['Platinum', 'Gold', 'Silver'];

function SponsorTile({ sponsor }: { sponsor: HackathonSponsorProps }) {
    return (
        <a
            href={sponsor.websiteLink}
            target="_blank"
            rel="noreferrer"
            className="w-full aspect-square rounded-[16px] border border-[#6E6E6E] bg-transparent overflow-hidden block"
        >
            {/* Fill the tile, rounded corners */}
            <img
                src={sponsor.logoSrc}
                alt={sponsor.name}
                draggable={false}
                className="w-full h-full object-cover rounded-[16px] select-none"
            />
        </a>
    );
}

function RankPanel({ rank, sponsors }: { rank: SponsorRank; sponsors: HackathonSponsorProps[] }) {
    const meta = RANK_META[rank];

    // Ranks outside the main design: only show if they exist.
    if (!meta.alwaysShow && sponsors.length === 0) return null;

    return (
        <section className="rounded-[22px] w-full" style={{ background: PANEL_BG }}>
            <div className="px-5 sm:px-8 pt-6 sm:pt-7 pb-7">
                <div
                    className="font-oxanium uppercase tracking-[0.55em] leading-none text-[22px] sm:text-[28px] lg:text-[36px]"
                    style={{ color: meta.color }}
                >
                    {meta.label}
                </div>

                <div className="h-[1px] bg-[#1D1B1A] w-full mt-4 sm:mt-6" />

                {/* Keep the panel visible even with 0 sponsors, but show no tiles */}
                {sponsors.length === 0 ? (
                    <div className="h-[120px] sm:h-[180px] lg:h-[280px]" />
                ) : (
                    <div
                        className="
                            grid mt-6 sm:mt-8
                            gap-x-[18px] sm:gap-x-[24px] lg:gap-x-[31px]
                            gap-y-[18px] sm:gap-y-[22px] lg:gap-y-[24px]
                            justify-items-start
                            grid-cols-[repeat(auto-fit,minmax(140px,1fr))]
                            sm:grid-cols-[repeat(auto-fit,minmax(180px,1fr))]
                            lg:grid-cols-[repeat(auto-fit,minmax(230px,230px))]
                        "
                    >
                        {sponsors.map((s) => (
                            <SponsorTile key={`${s.name}-${s.websiteLink}`} sponsor={s} />
                        ))}
                    </div>
                )}
            </div>
        </section>
    );
}

export function SponsorsCard({
    sponsorsSwitch,
    grouped,
}: {
    sponsorsSwitch: boolean;
    grouped: Record<SponsorRank, HackathonSponsorProps[]>;
}) {
    return (
        <div className="relative w-full overflow-hidden rounded-[24px] bg-[#FFFDF5] shadow-[0_18px_60px_rgba(0,0,0,0.45)] min-h-[1200px] sm:min-h-[1500px] lg:min-h-[1760px]">
            {/* Background flames */}
            <img
                src="/flames.png"
                alt="Flame Background"
                className="absolute inset-0 w-full h-full pointer-events-none select-none object-cover object-[50%_70%] md:object-contain md:object-center"
                draggable={false}
            />

            {/* Bars */}
            <VerticalBar isRight={true} isBlack={true} />
            <VerticalBar isRight={false} isBlack={true} />

            {/* Content */}
            <div
                className="relative  z-10 mx-auto max-w-[1400px]
                    px-10 sm:px-16 lg:px-24
                    pt-20 sm:pt-28 lg:pt-32
                    pb-16 sm:pb-24 lg:pb-32"
            >
                {/* Header */}
                <div className="flex items-center gap-[12px] sm:gap-[14px]">
                    <img
                        src="/mockingjay-red.svg"
                        alt="Sponsors-Icon"
                        className="w-[44px] h-[36px] sm:w-[52px] sm:h-[42px] select-none"
                        draggable={false}
                    />
                    <h2 className="font-orbitron text-[28px] sm:text-[34px] lg:text-[40px] leading-[100%] text-[#DA2F2F] whitespace-nowrap">
                        SPONSORS
                    </h2>
                </div>

                {!sponsorsSwitch ? (
                    <div className="mt-12 text-[#D11B1B] tracking-[0.25em] text-[16px] sm:text-[18px] lg:text-[22px] select-none">
                        SPONSORS COMING SOON . . .
                    </div>
                ) : (
                    <div className="mt-14 sm:mt-16 flex flex-col gap-12 sm:gap-16 lg:gap-20">
                        {/* Main ranks (always show panels) */}
                        {PRIMARY_RANKS.map((rank) => (
                            <div key={rank} className="w-full max-w-[1256px]">
                                <RankPanel rank={rank} sponsors={grouped[rank]} />
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Corner flame (optional; keep your asset) */}
            <img
                src="/hackathon8/sponsors/flame-corner.png"
                alt=""
                className="absolute pointer-events-none select-none hidden lg:block"
                style={{ right: -140, bottom: 40, width: 520 }}
                draggable={false}
            />
        </div>
    );
}
