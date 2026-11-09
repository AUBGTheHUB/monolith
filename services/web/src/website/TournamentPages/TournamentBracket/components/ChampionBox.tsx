import { getWinnerName, type BackendGroup } from '../types/bracket';

export function WinnerName({ name }: { name: string | null }) {
    return (
        <div className="flex h-12 w-full gap-1.5 2xl:h-14">
            <div className="flex min-w-0 flex-1 items-center bg-[#A39550] px-4">
                <span className="truncate font-oxanium text-base font-bold uppercase text-[#1A1A1A] 2xl:text-lg">
                    {name ?? '\u00A0'}
                </span>
            </div>
            <div className="flex w-12 items-center justify-center bg-white font-bold 2xl:w-14">-</div>
        </div>
    );
}

export function ChampionBox({ final }: { final?: BackendGroup }) {
    return (
        <div className="flex w-[24vw] min-w-[20rem] shrink-0 flex-col items-center bg-gradient-to-b from-[#E9D06A] to-[#F2C94C] py-12 [clip-path:polygon(0_0,100%_0,92%_100%,8%_100%)]">
            <div className="flex h-[var(--head)] flex-col items-center">
                <h2 className="font-oxanium text-6xl font-black tracking-wide text-black 2xl:text-7xl">WINNER</h2>
                <img src="/trophy.svg" alt="" className="mt-3 h-14 w-14 2xl:h-16 2xl:w-16" draggable={false} />
            </div>
            <div className="flex w-full flex-1 items-center px-[12%]">
                <WinnerName name={getWinnerName(final)} />
            </div>
        </div>
    );
}
