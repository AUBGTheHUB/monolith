import { MatchBox } from './MatchBox';
import { ROUND_TITLES, findGroup, slotsInRound, type BackendGroup } from '../types/bracket';

function Connector({ single }: { single: boolean }) {
    // final
    if (single) return <span className="absolute left-full top-1/2 w-[var(--gap)] border-t border-white/70" />;
    return (
        <>
            {/* "]" joining the centres of the two matches*/}
            <span className="absolute left-full top-1/4 h-1/2 w-[calc(var(--gap)/2)] border-y border-r border-white/70" />
            {/* line from the middle of "]" to the next round*/}
            <span className="absolute left-[calc(100%+var(--gap)/2)] top-1/2 w-[calc(var(--gap)/2)] border-t border-white/70" />
        </>
    );
}

export function BracketRound({ round, groups }: { round: number; groups: BackendGroup[] }) {
    const slots = slotsInRound(round);
    const single = slots === 1;
    // round 1 -> [[1,2],[3,4]], round 2 -> [[1,2]], round 3 -> [[1]]
    const pairs = single ? [[1]] : Array.from({ length: slots / 2 }, (_, i) => [2 * i + 1, 2 * i + 2]);

    return (
        <div className="flex min-w-0 flex-1 flex-col">
            <div className="h-[var(--head)]">
                <h3 className="text-center font-oxanium text-2xl font-bold tracking-wide text-[#F2C94C] 2xl:text-3xl">
                    {ROUND_TITLES[round - 1]}
                </h3>
            </div>
            <div className="flex flex-1 flex-col">
                {pairs.map((pair) => (
                    <div key={pair[0]} className="relative flex flex-1 flex-col justify-around">
                        {pair.map((n) => (
                            <MatchBox key={n} group={findGroup(groups, round, n)} />
                        ))}
                        <Connector single={single} />
                    </div>
                ))}
            </div>
        </div>
    );
}
