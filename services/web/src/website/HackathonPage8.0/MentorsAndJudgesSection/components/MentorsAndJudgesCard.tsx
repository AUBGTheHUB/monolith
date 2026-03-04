import { cn } from '@/lib/utils';
import { Linkedin } from 'lucide-react';
import { Link } from 'react-router';

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
                <Link to={linkedin_url} target="_blank">
                    <Linkedin
                        strokeWidth={'2px'}
                        className="h-6 w-auto absolute top-4 right-4 bg-[#FBAF45] rounded-sm p-[2px]"
                        color="#1B1919"
                    />
                </Link>
            )}

            <img src={avatar_url} className="absolute inset-0 w-full h-full object-cover object-top" />

            <div className="absolute right-0 bottom-[42px] pl-[16px] bg-[#1B1919] opacity-91 w-[230px] h-[80px] flex items-center justify-between pr-4">
                <div className="flex flex-col items-start justify-center">
                    <span className="font-orbitron text-[18px] tracking-widest font-semibold">{name}</span>
                    <span className="font-oxanium text-[12px] text-[#FBAF45]">
                        {job_title ? `${job_title} | ` : ''}
                        {company}
                    </span>
                </div>
            </div>
        </div>
    );
}
