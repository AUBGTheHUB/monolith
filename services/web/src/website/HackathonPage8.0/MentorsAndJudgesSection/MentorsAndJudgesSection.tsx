import { VerticalBar } from '@/components/ui/verticalBar';
import redPin from './assets/red-pin.svg';
import yellowPin from './assets/yellow-pin.svg';
import { Carousel } from './components/Caroussel';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/services/apiClient';
import { Mentor } from '@/types/mentor';
import { Judge } from '@/types/judge';

export const MentorsAndJudgesSection = () => {
    const { data: mentors } = useQuery({
        queryKey: ['hackaton', 'mentors', 'carousel'],
        queryFn: () => apiClient.get<{ mentors: Mentor[] }>('/admin/mentors'),
        select: (res) => res.mentors,
    });

    const { data: judges } = useQuery({
        queryKey: ['hackaton', 'judges', 'carousel'],
        queryFn: () => apiClient.get<{ judges: Judge[] }>('/admin/judges'),
        select: (res) => res.judges,
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

            <div className="flex flex-col items-center justify-center gap-[100px]">
                <Carousel title="MENTORS" imgSrc={yellowPin} data={mentors} />
                <Carousel title="JURY" imgSrc={redPin} data={judges} />
            </div>
        </section>
    );
};
