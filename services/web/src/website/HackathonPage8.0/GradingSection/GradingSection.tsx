import { GradingCard } from './GradingCard';
import { bottomRowData, topRowData } from './data.ts';
import { VerticalBar } from '@/components/ui/verticalBar';

export const GradingSection = () => {
    return (
        <section className="relative w-full min-h-dvh flex flex-col items-center justify-center py-[5vh] bg-[#FFFDF5] overflow-hidden">
            <img
                src="/GradingFireTL.png"
                alt="Fire decoration"
                className="absolute top-0 left-0 w-[300px] lg:w-[30vw] opacity-90 z-0 pointer-events-none mix-blend-multiply"
            />
            <img
                src="/GradingFireBR.png"
                alt="Fire decoration"
                className="absolute bottom-0 right-0 w-[300px] lg:w-[35vw] opacity-90 z-0 pointer-events-none mix-blend-multiply"
            />

            <VerticalBar isRight={false} isBlack={true} />
            <VerticalBar isRight={true} isBlack={true} />

            <div
                className="relative z-10 w-full flex flex-col items-center gap-[4vh] px-6"
                style={{
                    maxWidth: 'clamp(40rem, 82vw, 80rem)',
                }}
            >
                <div className="w-full flex items-center justify-start gap-4 lg:gap-6">
                    <img
                        src="/gradingLogoicon.png"
                        alt="Logo Icon"
                        className="w-10 h-10 lg:w-[6vh] lg:h-[6vh] object-contain"
                    />
                    <h2 className="text-black text-3xl lg:text-[4.5vh] font-orbitron font-bold tracking-[0.1em] uppercase">
                        Grading Criteria
                    </h2>
                </div>

                <div className="w-full flex flex-col gap-[4vh]">
                    <GradingCard left={topRowData.left} right={topRowData.right} isDarkTop={true} />

                    <GradingCard left={bottomRowData.left} right={bottomRowData.right} isDarkTop={false} />
                </div>

                <a
                    href="#" // add actual PDF link here
                    className="mt-4 text-black/70 font-oxanium underline text-sm lg:text-[2vh] hover:text-black transition-colors"
                >
                    Download PDF Version Here
                </a>
            </div>
        </section>
    );
};
