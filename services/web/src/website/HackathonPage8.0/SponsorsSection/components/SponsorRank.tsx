import { SponsorCard } from './SponsorCard';
import type { Sponsor } from '../types/constatns';
import { SPONSOR_RANK_META, type SponsorRank } from '../types/constatns';

export function SponsorRankSection({ rank, sponsors }: { rank: SponsorRank; sponsors: Sponsor[] }) {
    if (!sponsors.length) return null;

    const { color, label } = SPONSOR_RANK_META[rank];

    return (
        <div
            className="mt-6 sm:mt-10 rounded-2xl overflow-hidden
           bg-gradient-to-r from-white/95 via-white/85 to-white/60"
        >
            <div className="px-4 sm:px-10 py-4 sm:py-6">
                <h3
                    className="font-oxanium uppercase tracking-[0.35em] sm:tracking-[0.55em] leading-none
             text-[22px] sm:text-[28px] lg:text-[36px]"
                    style={{ color }}
                >
                    {label}
                </h3>

                <div className="w-full h-px bg-black/80 mt-3 sm:mt-4 mb-4 sm:mb-6" />

                <div className="grid grid-cols-1 sm:grid-cols-5 gap-4 sm:gap-3 place-items-center sm:place-items-stretch">
                    {sponsors.map((sponsor) => (
                        <SponsorCard sponsor={sponsor} key={sponsor.id ?? sponsor.name} rank={rank} />
                    ))}
                </div>
            </div>
        </div>
    );
}
