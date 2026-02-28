import { SectionTitle } from '../shared/SectionTitle';

const YOUTUBE_EMBED_URL = 'https://www.youtube.com/embed/UAE_0mkBYi0?si=cK_Jg0drEen2K2Wt';

export const RecapSection = () => {
    return (
        <section id="recap" className="relative w-full overflow-hidden bg-[#151313]">
            <div
                className="absolute inset-0 bg-cover bg-center opacity-[0.25]"
                style={{ backgroundImage: "url('/rocksBG.png')" }}
            />

            <div
                className="relative z-10 w-full mx-auto px-8 md:px-0 pt-16 pb-16 md:pt-28 md:pb-32 flex flex-col gap-16 md:gap-28"
                style={{ maxWidth: 'clamp(40rem, 82vw, 80rem)' }}
            >
                <SectionTitle title="HACKATHON 7.0" iconSrc="/orange_icon.svg" iconAlt="Recap icon" dark />

                <div className="relative w-full aspect-video rounded-[20px] overflow-hidden bg-black/20">
                    <iframe
                        className="absolute inset-0 w-full h-full border-0"
                        src={YOUTUBE_EMBED_URL}
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowFullScreen
                        loading="lazy"
                        sandbox="allow-scripts allow-same-origin allow-presentation"
                        title="HACKAUBG 7.0 Recap"
                    />
                </div>
            </div>
        </section>
    );
};
