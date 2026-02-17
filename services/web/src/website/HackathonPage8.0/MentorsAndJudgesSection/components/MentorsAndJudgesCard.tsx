import { cn } from '@/lib/utils';

interface MentorsAndJudgesCardProps {
    name: string;
    company: string;
    avatar_url: string;
    job_title?: string;
    className?: string;
    isLoading?: boolean;
}

export function MentorsAndJudgesCard({ className, name, job_title, company, avatar_url }: MentorsAndJudgesCardProps) {
    return (
        <div className={cn('relative h-[295px] w-[255px] rounded-3xl border border-white overflow-hidden', className)}>
            <img src={avatar_url} className="object-fill" />

            <div className="absolute right-0 bottom-[42px] pl-[16px] bg-[#1B1919] opacity-91 w-[230px] h-[80px] flex flex-col items-start justify-center">
                <span className="font-orbitron text-[18px] tracking-widest font-semibold">{name}</span>
                <span className="font-oxanium text-[12px] text-[#FBAF45]">
                    {job_title ? `${job_title} | ` : ''}
                    {company}
                </span>
            </div>
        </div>
    );
}
