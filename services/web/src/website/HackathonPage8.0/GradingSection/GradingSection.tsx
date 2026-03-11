import { GradingCard } from './GradingCard';
import { bottomRowData, topRowData } from './data.ts';
import { SectionTitle } from '../shared/SectionTitle';

export const GradingSection = () => {
    return (
        <section
            id="grading-criteria"
            className="relative w-full min-h-dvh flex flex-col items-center justify-center py-[5vh] bg-[#FFFDF5] overflow-hidden"
        >
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

            <div
                className="relative z-10 w-full mx-auto flex flex-col items-center gap-[4vh] px-8 md:px-0"
                style={{ maxWidth: 'clamp(40rem, 82vw, 80rem)' }}
            >
                <div className="w-full">
                    <SectionTitle
                        title="GRADING CRITERIA"
                        iconSrc="/gradingLogoicon.png"
                        iconAlt="Grading icon"
                        dark={false}
                    />
                </div>

                <div className="w-full flex flex-col gap-[4vh]">
                    <GradingCard left={topRowData.left} right={topRowData.right} isDarkTop={true} />

                    <GradingCard left={bottomRowData.left} right={bottomRowData.right} isDarkTop={false} />
                </div>
            </div>
        </section>
    );
};
