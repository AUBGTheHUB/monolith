import type { Sponsor, SponsorRank } from '../types/constatns';
import { SPONSOR_RANK_META } from '../types/constatns';

export function SponsorCard({ sponsor, rank }: { sponsor: Sponsor; rank: SponsorRank }) {
    const hover = SPONSOR_RANK_META[rank].hoverShadowClass;

    return (
        <a
            href={sponsor.websiteLink}
            target="_blank"
            rel="noreferrer"
            className={[
                'group block rounded-xl bg-white',
                'border border-black/10',
                'transition-all duration-300',
                'hover:-translate-y-[1px] hover:shadow-lg',
                hover,
                'w-full max-w-[16rem] mx-auto',
                'sm:max-w-none sm:mx-0',
                'aspect-square p-3 sm:p-5',
            ].join(' ')}
        >
            <img src={sponsor.logoSrc} alt={sponsor.name} className="w-full h-full object-contain" />
        </a>
    );
}
