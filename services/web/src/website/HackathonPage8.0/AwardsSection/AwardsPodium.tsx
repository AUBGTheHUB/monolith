import { awards } from './awardsConfig';
import { AwardCard } from './AwardCard';

export const AwardsPodium = () => {
    const sortedAwards = awards.slice().sort((a, b) => {
        const order = [2, 1, 3];
        return order.indexOf(a.position) - order.indexOf(b.position);
    });

    return (
        <div className="w-full flex justify-center items-center relative z-10 mb-[4vh] flex-1">
            <div className="flex flex-col lg:flex-row items-center justify-center gap-6 lg:gap-[2vw] px-4 xl:mr-[75px]">
                {sortedAwards.map((award) => (
                    <AwardCard key={award.position} {...award} />
                ))}
            </div>
        </div>
    );
};
