import { useEffect, useState } from 'react';
import './LandingSection.css';

const HACK_LETTERS = ['H', 'A', 'C', 'K'];
const AUBG_LETTERS = ['A', 'U', 'B', 'G'];

export default function LandingSection() {
    const [mounted, setMounted] = useState(false);

    useEffect(() => {
        const timer = setTimeout(() => setMounted(true), 100);
        return () => clearTimeout(timer);
    }, []);

    return (
        <div className="bg-[rgba(255,253,245,1)] h-[calc(100dvh-10dvh)] md:h-[calc(100dvh-5rem)] overflow-hidden">
            <img
                src="/hackLanding8.0/leftFlame.webp"
                alt=""
                style={mounted ? { animation: 'fadeIn 1s ease-out 0.1s both' } : { opacity: 0 }}
                className="absolute pointer-events-none block bottom-[0] h-[30rem] top-[-3rem] md:h-[55rem] md:top-[-7rem] z-0"
            />
            <img
                src="/hackLanding8.0/rightFlame.webp"
                alt=""
                style={mounted ? { animation: 'fadeIn 1s ease-out 0.4s both' } : { opacity: 0 }}
                className="absolute pointer-events-none bottom-[0] block h-[25rem] right-[0] md:h-[45rem] z-0"
            />

            <div className="h-full flex justify-center items-center pb-[10dvh] md:pb-[5rem]">
                <div className="font-orbitron z-10">
                    <div className="flex flex-col items-center justify-center text-center gap-1 sm:gap-2 lg:gap-3">
                        {/* THE HUB'S */}
                        <p
                            style={
                                mounted
                                    ? { animation: 'slideUpFade 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.1s both' }
                                    : { opacity: 0 }
                            }
                            className="text-xl xs:text-lg sm:text-2xl md:text-3xl lg:text-4xl xl:text-5xl tracking-[0.3em] font-semibold text-[rgb(49,46,46)]"
                        >
                            THE HUB&apos;S
                        </p>

                        {/* HACK — letter-by-letter drop, then fire flicker */}
                        <h1
                            className="flex leading-none"
                            style={mounted ? { animation: 'flicker 5s ease-in-out infinite 2s' } : {}}
                        >
                            {HACK_LETTERS.map((letter, i) => (
                                <span
                                    key={i}
                                    style={
                                        mounted
                                            ? {
                                                  animation: `letterDrop 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) ${0.4 + i * 0.09}s both`,
                                              }
                                            : { opacity: 0 }
                                    }
                                    className="text-7xl sm:text-8xl md:text-9xl lg:text-[10rem] xl:text-[12rem] bg-clip-text text-transparent bg-[radial-gradient(circle_at_50%_0%,_#FBC42C_0.1%,_#F6741C_50%,_#D91313_100%)] font-extrabold transform-gpu"
                                >
                                    {letter}
                                </span>
                            ))}
                        </h1>

                        {/* AUBG + 8.0 */}
                        <div className="flex flex-col sm:flex-row sm:gap-5 lg:gap-8">
                            <h2 className="flex leading-none">
                                {AUBG_LETTERS.map((letter, i) => (
                                    <span
                                        key={i}
                                        style={
                                            mounted
                                                ? {
                                                      animation: `letterDrop 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) ${0.76 + i * 0.09}s both`,
                                                  }
                                                : { opacity: 0 }
                                        }
                                        className="text-7xl sm:text-8xl md:text-9xl lg:text-[10rem] xl:text-[12rem] bg-clip-text text-transparent bg-[radial-gradient(circle_at_70%_0%,_#F6741C_0.1%,_#D91313_60%,_#AA1616_100%)] font-extrabold transform-gpu"
                                    >
                                        {letter}
                                    </span>
                                ))}
                            </h2>

                            <h2
                                style={
                                    mounted
                                        ? { animation: `letterDrop 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) 1.12s both` }
                                        : { opacity: 0 }
                                }
                                className="text-7xl sm:text-8xl md:text-9xl lg:text-[10rem] xl:text-[12rem] bg-clip-text text-transparent bg-[radial-gradient(circle_at_0%_0%,_#D91313_60%,_#AA1616_70%)] font-extrabold leading-none transform-gpu"
                            >
                                8.0
                            </h2>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
