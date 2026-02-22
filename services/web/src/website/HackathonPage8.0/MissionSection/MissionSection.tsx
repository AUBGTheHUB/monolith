import { VerticalBar } from '@/components/ui/verticalBar';
import { MissionItem } from './MissionItem';

export const MissionSection = () => {
    return (
        <section id="mission" className="relative w-full rounded-t-[20px] overflow-hidden bg-[#151313]">
            <div
                className="absolute inset-0 bg-cover bg-center blur-[0.4px] opacity-[0.25]"
                style={{ backgroundImage: "url('/rocksBG.png')" }}
            />

            <VerticalBar isRight={true} isBlack={false} />
            <VerticalBar isRight={false} isBlack={false} />

            <div className="relative z-10 grid place-items-center px-8 py-20 md:py-48">
                <div
                    className="
                        w-full
                        flex
                        flex-col
                        gap-9
                    "
                    style={{
                        maxWidth: 'clamp(40rem, 82vw, 80rem)',
                    }}
                >
                    <div className="flex items-center gap-[5px]">
                        <img src="/yellow_icon.svg" alt="Mission icon" className="h-[42px] w-auto" />
                        <h2 className="font-orbitron text-[40px] leading-[1] tracking-[0.3em] text-[#FFFDF5]">
                            MISSION
                        </h2>
                    </div>

                    <MissionItem />
                </div>
            </div>
        </section>
    );
};
