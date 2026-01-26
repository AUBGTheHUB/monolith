import { AwardsHeader } from './AwardsHeader';
import { AwardsPodium } from './AwardsPodium';
import { AwardsFooter } from './AwardsFooter';

export const AwardsSection = () => {
    return (
        <section
            className="w-full h-dvh flex flex-col items-center justify-center py-8 relative bg-black before:absolute before:inset-0 before:bg-black before:opacity-70 before:z-0 rounded-t-lg overflow-hidden"
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
