import { cn } from '@/lib/utils';
import type { BackendGroup } from '../types/bracket';

function TeamRow({ name, isWinner }: { name?: string | null; isWinner: boolean }) {
    return (
        <div className="flex h-12 gap-1.5 2xl:h-14">
            <div
                className={cn(
                    'flex min-w-0 flex-1 items-center bg-[#0E1E2E]/80 px-4 transition-shadow duration-300',
                    isWinner && 'ring-1 ring-[#F2C94C] shadow-[0_0_14px_2px_#F2C94C]',
                )}
            >
                <span className="truncate font-oxanium text-base font-bold uppercase tracking-wide text-[#F2C94C] 2xl:text-lg">
                    {name ?? '\u00A0'}
                </span>
            </div>
            <div className="flex w-12 items-center justify-center bg-white font-bold text-[#0B1E33] 2xl:w-14">-</div>
        </div>
    );
}

export function MatchBox({ group }: { group?: BackendGroup }) {
    return (
        <div className="flex w-full flex-col gap-1.5">
            <TeamRow name={group?.first} isWinner={group?.winner === 'first'} />
            <TeamRow name={group?.second} isWinner={group?.winner === 'second'} />
        </div>
    );
}
