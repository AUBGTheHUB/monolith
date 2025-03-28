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
                className={`flex flex-col min-w-28 max-w-80 max-[1122px]:max-w-full h-70 p-2 border-[1px] rounded-[15px] border-[rgb(255,255,255,0.2)] font-semibold transition-opacity duration-500 ease-in-out ${isLoaded ? 'opacity-100' : 'opacity-0'}`}
            >
                <div className="h-5/6 w-full">
                    <img src={imgSrc} alt={name} className="object-cover w-full h-full rounded-xl" />
                </div>
                <div className="h-1/6 py-3 gap-2">
                    <h3 className="text-secondary line-clamp-1">{name}</h3>
                </div>
            </div>
        </>
    );
}
