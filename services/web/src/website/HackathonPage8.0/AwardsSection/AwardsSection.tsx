import { VerticalBar } from '@/components/ui/verticalBar';
import { AwardsFooter, AwardsHeader, AwardsPodium } from './AwardItem';

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
            <div className="absolute inset-0 z-50 pointer-events-none">
                <VerticalBar isRight={false} isBlack={false} />
                <VerticalBar isRight={true} isBlack={false} />
            </div>

            <AwardsHeader />
            <AwardsPodium />
            <AwardsFooter />
        </section>
    );
};
