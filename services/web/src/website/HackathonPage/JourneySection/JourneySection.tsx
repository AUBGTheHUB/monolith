import { useRef, useLayoutEffect } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/dist/ScrollTrigger';
import JourneyModule from './JourneyModule';
import journeyEntries from './StaticContent/journeyEntries.json';

gsap.registerPlugin(ScrollTrigger);

function JourneySection() {
    const triggerRef = useRef<HTMLDivElement>(null);
    const itemsRef = useRef<HTMLDivElement[]>([]);
    const mm = gsap.matchMedia();

    // Helper to add each element to the ref array
    const addToRefs = (el: HTMLDivElement) => {
        if (el && !itemsRef.current.includes(el)) {
            itemsRef.current.push(el);
        }
    };

    useLayoutEffect(() => {
        const ctx = gsap.context(() => {
            mm.add(
                {
                    isMobile: '(max-width: 768px)', // Mobile
                    isDesktop: '(min-width: 769px)', // Desktop
                },
                (context) => {
                    const { isMobile } = context.conditions as { isMobile: boolean };

                    const startOffset = isMobile ? 50 : 220;
                    const finishOffset = isMobile ? 4 : 8;

                    // Kill previous animations if any
                    gsap.killTweensOf(itemsRef.current);

                    gsap.fromTo(
                        itemsRef.current,
                        {
                            x: (i: number) => `${startOffset + i * 60}vh`,
                        },
                        {
                            x: (i: number) => `${isMobile ? finishOffset : finishOffset + i * 5}rem`,
                            ease: 'none',
                            duration: 1,
                            stagger: 0.3,
                            scrollTrigger: {
                                trigger: triggerRef.current,
                                start: 'top top',
                                end: '2000 top',
                                scrub: 0.6,
                                pin: true,
                                toggleActions: 'play none none reverse',
                            },
                        },
                    );
                },
            );
        });

        return () => {
            ctx.revert(); // Cleanup on unmount
            mm.revert(); // Revert MatchMedia listeners
        };
    }, []);

    return (
        <div className="w-full relative">
            <div className="sticky h-[50rem] top-0 z-50 pt-[10rem] ml-[9%] bg-transparent">
                <div className="sm:text-4xl text-3xl sm:mb-20 mb-10 flex items-center space-x-4 p-4">
                    <img src="./JourneySection/symbol.svg" alt="" className="w-[1.6rem]" />
                    <p className="text-white tracking-[0.2em]">JOURNEY</p>
                </div>
            </div>
            <section className="scroll-section-outer mr-20 gap-[20rem] min-h-[40rem]">
                <div ref={triggerRef} className="mr-0 relative w-full h-screen">
                    {journeyEntries.map((entry, index) => (
                        <div
                            key={index}
                            ref={addToRefs}
                            className="absolute top-0 left-0 w-full"
                            style={{ zIndex: index + 1 }}
                        >
                            <JourneyModule title={entry.title} text={entry.text} />
                        </div>
                    ))}
                </div>
            </section>
        </div>
    );
}

export default JourneySection;
