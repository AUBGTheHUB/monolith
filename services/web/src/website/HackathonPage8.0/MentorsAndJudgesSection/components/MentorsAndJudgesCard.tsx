import { cn } from '@/lib/utils';
import { Linkedin } from 'lucide-react';

interface MentorsAndJudgesCardProps {
    name: string;
    company: string;
    avatar_url: string;
    job_title?: string;
    linkedin_url?: string;
    className?: string;
    isLoading?: boolean;
}

export function MentorsAndJudgesCard({
    className,
    name,
    job_title,
    company,
    avatar_url,
    linkedin_url,
}: MentorsAndJudgesCardProps) {
    return (
        <div className={cn('relative h-[295px] w-[255px] rounded-3xl border border-white overflow-hidden', className)}>
            {linkedin_url && (
                <a href={linkedin_url} target="_blank" rel="noreferrer" aria-label={`Open ${name}'s LinkedIn profile`}>
                    <Linkedin
                        strokeWidth={'2px'}
                        className="h-6 w-auto absolute top-4 right-4 bg-[#FBAF45] rounded-sm p-[2px] z-10"
                        color="#1B1919"
                    />
                </a>
            )}

            <img src={avatar_url} className="absolute inset-0 w-full h-full object-cover object-top" />

            <div
                className="absolute right-0 bottom-[16px] pl-[14px] w-[220px] h-[70px] flex items-center justify-between pr-3"
                style={{ backgroundColor: 'rgba(27, 25, 25, 0.85)' }}
            >
                <div className="flex flex-col items-start justify-center">
                    <span className="font-orbitron text-[16px] tracking-[0.18em] font-semibold leading-tight">
                        {name}
                    </span>
                    <span className="font-oxanium text-[11px] text-[#FBAF45] leading-snug">
                        {job_title ? `${job_title} | ` : ''}
                        {company}
                    </span>
                </div>
            </div>
        </div>
    );
}
