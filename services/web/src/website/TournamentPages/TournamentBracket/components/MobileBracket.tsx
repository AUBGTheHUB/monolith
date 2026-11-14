import { MatchBox } from './MatchBox';
import { WinnerName } from './ChampionBox';
import {
    ROUND_TITLES,
    TOTAL_ROUNDS,
    findGroup,
    getWinnerName,
    slotsInRound,
    type BackendGroup,
} from '../types/bracket';
import { cn } from '@/lib/utils';

function WinnerCard({ name }: { name: string | null }) {
    return (
        <div className="mx-auto flex max-w-sm flex-col items-center bg-gradient-to-b from-[#E9D06A] to-[#F2C94C] px-8 pb-10 pt-6 [clip-path:polygon(0_0,100%_0,94%_100%,6%_100%)]">
            <h2 className="font-oxanium text-4xl font-black tracking-wide text-black sm:text-5xl">WINNER</h2>
            <img src="/trophy.svg" alt="" className="mt-2 h-10 w-10 sm:h-12 sm:w-12" draggable={false} />
            <div className="mt-5 w-full">
                <WinnerName name={name} />
            </div>
        </div>
    );
}

function RoundSection({ round, groups }: { round: number; groups: BackendGroup[] }) {
    const slots = slotsInRound(round);
    const bracketNumbers = Array.from({ length: slots }, (_, i) => i + 1);

    return (
        <section className="mt-10">
            <h3 className="mb-4 flex items-center gap-3 font-oxanium text-xl font-bold tracking-wide text-[#F2C94C]">
                {ROUND_TITLES[round - 1]}
                <span className="h-px flex-1 bg-[#F2C94C]/30" aria-hidden />
            </h3>
            <div className={cn('grid gap-4', slots > 1 && 'sm:grid-cols-2')}>
                {bracketNumbers.map((n) => (
                    <MatchBox key={n} group={findGroup(groups, round, n)} />
                ))}
            </div>
        </section>
    );
}

export function MobileBracket({ groups }: { groups: BackendGroup[] }) {
    // newest round first: FINALS, SEMI-FINALS, QUARTER-FINALS
    const rounds = Array.from({ length: TOTAL_ROUNDS }, (_, i) => TOTAL_ROUNDS - i);

    return (
        <div className="min-h-screen bg-[linear-gradient(180deg,#0A1C30_0%,#081A2E_60%,#1F3F5C_100%)] px-4 py-8 text-white sm:px-8">
            <WinnerCard name={getWinnerName(findGroup(groups, TOTAL_ROUNDS, 1))} />
            {rounds.map((r) => (
                <RoundSection key={r} round={r} groups={groups} />
            ))}
        </div>
    );
}
