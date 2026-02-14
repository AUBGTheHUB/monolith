import { VerticalBar } from '@/components/ui/verticalBar';
import { RecapVideo } from './RecapVideo';

export const RecapSection = () => {
    return (
        <section id="recap" className="relative w-full rounded-[20px] overflow-hidden bg-[#151313]">
            <div
                className="absolute inset-0 bg-cover bg-center blur-[0.4px] opacity-[0.25]"
                style={{ backgroundImage: "url('/rocksBG.png')" }}
            />

            <VerticalBar isRight={true} isBlack={false} />
            <VerticalBar isRight={false} isBlack={false} />

            <div className="relative z-10 grid place-items-center px-5 sm:px-8 pt-16 pb-16 md:pt-28 md:pb-32">
                <div
                    className="w-full flex flex-col"
                    style={{
                        maxWidth: 'clamp(20rem, 82vw, 80rem)',
                    }}
                >
                    <div className="flex items-center gap-[5px] max-w-full">
                        <img src="/orange_icon.svg" alt="Recap icon" className="h-[42px] w-auto shrink-0" />
                        <h2
                            className="
                                font-orbitron
                                text-[24px]
                                sm:text-[40px]
                                leading-[1]
                                tracking-[0.12em]
                                sm:tracking-[0.3em]
                                text-[#FFFDF5]
                                whitespace-nowrap
                            "
                        >
                            HACKATHON 7.0
                        </h2>
                    </div>

                    <div className="mt-16 md:mt-28">
                        <RecapVideo />
                    </div>
                </div>
            </div>
        </section>
    );
};
