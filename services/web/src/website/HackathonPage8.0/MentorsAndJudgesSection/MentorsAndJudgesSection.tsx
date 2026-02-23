import { VerticalBar } from '@/components/ui/verticalBar';
import redPin from './assets/red-pin.svg';
import yellowPin from './assets/yellow-pin.svg';
import { Carousel } from './components/Caroussel';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/services/apiClient';
import { Mentor } from '@/types/mentor';
import { Judge } from '@/types/judge';

interface MentorsAndJudgesProps {
    mentorsSwitch: boolean;
    jurySwitch: boolean;
}

export const MentorsAndJudgesSection = ({ mentorsSwitch, jurySwitch }: MentorsAndJudgesProps) => {
    const { data: mentors } = useQuery({
        queryKey: ['hackaton', 'mentors', 'carousel'],
        queryFn: () => apiClient.get<{ mentors: Mentor[] }>('/admin/mentors'),
        select: (res) => res.mentors,
        enabled: mentorsSwitch,
    });

    const { data: judges } = useQuery({
        queryKey: ['hackaton', 'judges', 'carousel'],
        queryFn: () => apiClient.get<{ judges: Judge[] }>('/admin/judges'),
        select: (res) => res.judges,
        enabled: jurySwitch,
    });

    return (
        <section id="mentors-and-judges" className="relative text-white w-full py-28 overflow-hidden bg-[#151313]">
            {/* BACKGROUND PHOTO */}
            <div
                className="absolute pointer-events-none inset-0 bg-cover bg-center blur-[0.4px] opacity-[0.25]"
                style={{ backgroundImage: "url('/rocksBG.png')" }}
            />

            <VerticalBar isRight={true} isBlack={false} />
            <VerticalBar isRight={false} isBlack={false} />

            <div className="flex flex-col items-center justify-center gap-[100px] relative z-10">
                {/* MENTORS SECTION */}
                <Carousel title="MENTORS" imgSrc={yellowPin} data={mentors || []} />
                {!mentorsSwitch && (
                    <p className="mt-4 text-gray-500 italic font-medium tracking-widest animate-pulse">
                        REVEALING SOON...
                    </p>
                )}

                {/* JURY SECTION */}
                <Carousel title="JURY" imgSrc={redPin} data={judges || []} />
                {!jurySwitch && (
                    <p className="mt-4 text-gray-500 italic font-medium tracking-widest animate-pulse">
                        REVEALING SOON...
                    </p>
                )}
            </div>
        </section>
    );
};
