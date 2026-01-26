import { AwardCard } from './AwardCard';
import { awards } from './awardsConfig';

export const AwardsPodium = () => (
    <div className="w-full flex justify-center relative z-10 mb-16 lg:mb-24 xl:mb-36">
        <div className="flex flex-col lg:flex-row items-center gap-8 lg:gap-[3vw] xl:gap-20 xl:mr-[75px] px-4">
            {awards.map((award) => (
                <AwardCard key={award.title} {...award} />
            ))}
        </div>
    </div>
);
