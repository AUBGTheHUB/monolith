import { useEffect, useState } from 'react';

export default function LandingSection() {
    const [fadeIn, setFadeIn] = useState(false);
    useEffect(() => {
        const timer = setTimeout(() => {
            setFadeIn(true);
        }, 400);

        return () => clearTimeout(timer);
    }, []);

    return (
        <div
            className={`bg-[rgba(255,253,245,1)] h-[90vh] transform transition-all duration-1000 ease-in-out ${fadeIn ? 'opacity-100' : 'opacity-0'}`}
        >
            <img
                src="/hackLanding8.0/leftFlame.webp"
                alt=""
                className="absolute pointer-events-none block  bottom-[0] h-[55rem] top-[-7rem] z-0"
            />
            <img
                src="/hackLanding8.0/rightFlame.webp"
                alt=""
                className="absolute pointer-events-none top-[10rem] xs:top-[0] block h-[45rem] right-[0] z-0"
            />

            <div className="h-full flex justify-center items-center">
                <div className="font-orbitron z-10">
                    <div className="flex flex-col items-center justify-center text-center gap-1">
                        <p className="text-sm xs:text-lg md:text-3xl tracking-[0.3em] font-semibold text-[rgb(49,46,46)] transform-gpu">
                            THE HUB&apos;S
                        </p>
                        <h1 className="text-6xl bg-clip-text text-transparent bg-[radial-gradient(circle_at_50%_0%,_#FBC42C_0.1%,_#F6741C_50%,_#D91313_100%)] font-extrabold drop-shadow-md md:text-8xl  transform-gpu">
                            HACK
                        </h1>
                        <div className="flex flex-col sm:flex-row sm:gap-5 ">
                            <h2 className="text-6xl bg-clip-text text-transparent bg-[radial-gradient(circle_at_70%_0%,_#F6741C_0.1%,_#D91313_60%,_#AA1616_100%)] font-extrabold drop-shadow-md md:text-8xl  transform-gpu">
                                AUBG
                            </h2>
                            <h2 className="text-6xl bg-clip-text text-transparent bg-[radial-gradient(circle_at_0%_0%,_#D91313_60%,_#AA1616_70%)] font-extrabold drop-shadow-md md:text-8xl  transform-gpu">
                                8.0
                            </h2>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
