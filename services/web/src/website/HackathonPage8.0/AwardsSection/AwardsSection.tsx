import { awards } from './Awards.data';
import { AwardItem } from './AwardItem';

const AwardsHeader = () => (
    <div className="w-full flex items-center justify-center mb-[4vh] relative z-30 px-4 lg:px-8 xl:px-16">
        <div className="flex-1 h-[4px] lg:h-[6px] xl:h-[8px] bg-white" aria-hidden="true" />
        <h2 className="text-white text-[4vh] lg:text-[5vh] xl:text-[6vh] font-orbitron font-bold tracking-[0.4em] ml-4 lg:ml-16 xl:ml-22 mr-4 lg:mr-4 xl:mr-12 whitespace-nowrap">
            AWARDS
        </h2>
        <div className="flex-1 h-[4px] lg:h-[6px] xl:h-[8px] bg-white" aria-hidden="true" />
    </div>
);

const AwardsPodium = () => {
    const sortedAwards = awards.slice().sort((a, b) => {
        const order = [2, 1, 3];
        return order.indexOf(a.position) - order.indexOf(b.position);
    });

    return (
        <div className="w-full flex justify-center items-center relative z-10 mb-[4vh] flex-1">
            <div className="flex flex-col lg:flex-row items-center justify-center gap-6 lg:gap-[2vw] px-4 xl:mr-[75px]">
                {sortedAwards.map((award) => (
                    <AwardItem key={award.position} {...award} />
                ))}
            </div>
        </div>
    );
};

const AwardsFooter = () => (
    <div className="flex flex-col items-center w-full relative z-30">
        <div className="flex flex-col lg:flex-row flex-wrap justify-between items-start w-full text-white text-[1.8vh] lg:text-[1.5vh] font-oxanium gap-[2vh] mb-[2vh] px-8 lg:px-[4vw] xl:px-32 leading-relaxed">
            <div className="flex-1 lg:max-w-[40%]">
                <p>And much more!</p>
                <p>Take part in all of the games we have prepared!</p>
            </div>
            <div className="flex-1 lg:text-right lg:max-w-[40%]">
                <p>All participants will receive giftbags with swag from The Hub and all HackAUBG 8.0 partners!</p>
            </div>
        </div>

        <div className="w-full flex items-center justify-center px-4 lg:px-8 xl:px-16">
            <div className="flex-1 h-[4px] lg:h-[6px] xl:h-[8px] bg-white" aria-hidden="true" />
            <div className="mx-6 lg:mx-[2vw] xl:mx-16">
                <img
                    src="/AwardsSection/HackAUBG_8.0-Awards-Logo.png"
                    alt="HackAUBG logo"
                    className="w-[4vh] h-[4vh] lg:w-[4vh] lg:h-[4vh] object-contain"
                />
            </div>
            <div className="flex-1 h-[4px] lg:h-[6px] xl:h-[8px] bg-white" aria-hidden="true" />
        </div>
    </div>
);

export const AwardsSection = () => {
    return (
        <section
            className="w-full min-h-dvh lg:h-dvh flex flex-col items-center justify-center py-12 lg:py-[3vh] relative bg-black before:absolute before:inset-0 before:bg-black before:opacity-70 before:z-0 rounded-t-lg"
            style={{
                backgroundImage: "url('/AwardsSection/HackAUBG_8.0-Awards-Background.png')",
                backgroundSize: 'cover',
                backgroundPosition: 'center',
                backgroundRepeat: 'no-repeat',
            }}
        >
            <div
                className="absolute left-4 lg:left-8 xl:left-16 top-0 bottom-0 w-[4px] lg:w-[6px] xl:w-[8px] bg-white z-20"
                aria-hidden="true"
            />
            <div
                className="absolute right-4 lg:right-8 xl:right-16 top-0 bottom-0 w-[4px] lg:w-[6px] xl:w-[8px] bg-white z-20"
                aria-hidden="true"
            />

            <AwardsHeader />
            <AwardsPodium />
            <AwardsFooter />
        </section>
    );
};
