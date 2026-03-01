import { MissionItem } from './MissionItem';
import { SectionTitle } from '../shared/SectionTitle';

export const MissionSection = () => {
    return (
        <section
            id="mission"
            className="relative w-full min-h-[80dvh] overflow-hidden bg-[#151313] flex items-center justify-center"
        >
            <div
                className="absolute inset-0 bg-cover bg-center blur-[0.4px] opacity-[0.25]"
                style={{ backgroundImage: "url('/rocksBG.png')" }}
            />

            <div
                className="relative z-10 w-full mx-auto px-8 md:px-0 flex flex-col gap-9"
                style={{ maxWidth: 'clamp(40rem, 82vw, 80rem)' }}
            >
                <SectionTitle title="MISSION" iconSrc="/yellow_icon.svg" iconAlt="Mission icon" dark />
                <MissionItem />
            </div>
        </section>
    );
};
