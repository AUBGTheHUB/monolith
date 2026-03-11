import { useState } from 'react';

type HubberModuleType = {
    imgSrc: string;
    name: string;
};

export default function HubberModule({ imgSrc, name }: HubberModuleType) {
    const [isLoaded, setIsLoaded] = useState(false);

    return (
        <>
            {!isLoaded && (
                <div className="hidden">
                    <img src={imgSrc} alt={name} onLoad={() => setIsLoaded(true)} />
                </div>
            )}

            <div
                className={`flex flex-col min-w-28 max-w-80 max-[1122px]:max-w-full h-auto p-2 border-[1px] rounded-[15px] border-[rgb(255,255,255,0.2)] font-semibold transition-opacity duration-500 ease-in-out ${
                    isLoaded ? 'opacity-100' : 'opacity-0'
                }`}
            >
                {/* Responsive Height:
                    - h-[240px] on mobile (taller/narrower look)
                    - md:h-[170px] on tablets and desktops (original look)
                */}
                <div className="relative h-[240px] md:h-[170px] w-full overflow-hidden rounded-xl">
                    {/* Background SVG - scaled up to cover all gaps */}
                    <img
                        src="/meetTheTeam/hubber-bg.svg"
                        alt=""
                        className="absolute inset-0 w-full h-full object-cover scale-110 -z-10"
                    />

                    {/* Main Portrait */}
                    <img src={imgSrc} alt={name} className="relative z-10 object-cover object-top w-full h-full" />
                </div>

                <div className="py-3 px-1">
                    <h3 className="text-secondary line-clamp-1">{name}</h3>
                </div>
            </div>
        </>
    );
}
