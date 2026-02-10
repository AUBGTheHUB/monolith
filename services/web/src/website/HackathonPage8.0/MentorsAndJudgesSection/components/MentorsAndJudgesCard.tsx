import { cn } from '@/lib/utils';

export function MentorsAndJudgesCard({ className }: { className?: string }) {
    /* TODO:
    - add props for the mentor/judge's name, title, company, and picture
    - add a background image for the card (from BE)
    */

    return (
        <div className={cn('relative h-[295px] w-[255px] rounded-3xl border border-white overflow-hidden', className)}>
            <img src="/schedule_bg.webp" className="object-fill" />

            <div className="absolute right-0 bottom-[42px] pl-[16px] bg-[#1B1919] opacity-91 w-[230px] h-[80px] flex flex-col items-start justify-center">
                <span className="font-orbitron text-[18px] tracking-widest font-semibold">John Doe</span>
                <span className="font-oxanium text-[12px] text-[#FBAF45]">CEO of Company | SoftServe</span>
            </div>
        </div>
    );
}
