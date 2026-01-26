import { awards } from './awardsConfig';
import { AwardCard } from './AwardCard';

export const AwardsPodium = () => {
    const sortedAwards = awards.slice().sort((a, b) => {
        const order = [2, 1, 3];
        return order.indexOf(a.position) - order.indexOf(b.position);
    });

    return (
        <div className="w-full flex justify-center relative z-10 mb-16 lg:mb-24 xl:mb-36">
            <div className="flex flex-col lg:flex-row items-center gap-8 lg:gap-[3vw] xl:gap-20 xl:mr-[75px] px-4">
                {sortedAwards.map((award) => (
                    <AwardCard key={award.position} {...award} />
                ))}
            </div>
        </div>
    );
};
