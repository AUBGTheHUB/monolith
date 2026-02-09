import { missionContent } from './data';

export const MissionItem = () => {
    return (
        <>
            <div
                className="
                    w-full
                    rounded-[20px]
                    px-10
                    py-8
                    font-oxanium
                    text-[22px]
                    leading-[1.4]
                    text-white
                "
                style={{
                    background: `linear-gradient(225deg, #FBB32D 2%, #F6741C 26%, #D91313 67%, #AA1616 100%)`,
                    backgroundSize: '200% 200%',
                    animation: 'moveGradient 10s ease infinite',
                    boxShadow: '0 20px 40px rgba(0,0,0,0.25)',
                }}
            >
                {missionContent.paragraphs.map((text, index) => (
                    <p key={index} className={index > 0 ? 'mt-6' : undefined}>
                        {text}
                    </p>
                ))}
            </div>

            <style>{`
                @keyframes moveGradient {
                    0% { background-position: 0% 50%; }
                    50% { background-position: 100% 50%; }
                    100% { background-position: 0% 50%; }
                }

                .hoverable-mission:hover {
                    transform: translateY(-4px);
                    transition: transform 250ms ease;
                }
            `}</style>
        </>
    );
};
