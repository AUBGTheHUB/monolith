import { useRef, useLayoutEffect, useEffect, useState, Fragment } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/dist/ScrollTrigger';
import { DesktopJourneyModule, MobileJourneyModule } from './JourneyModule';
import journeyEntries from './StaticContent/journeyEntries.json';

gsap.registerPlugin(ScrollTrigger);

function JourneySection() {
    const triggerRef = useRef<HTMLDivElement>(null);
    const itemsRef = useRef<HTMLDivElement[]>([]);
    const [isDesktop, setIsDesktop] = useState(window.innerWidth >= 768);

    useEffect(() => {
        const handleResize = () => {
            setIsDesktop(window.innerWidth >= 768);
        };

        window.addEventListener('resize', handleResize);

        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);
    // Helper function to add refs to items
    const addToRefs = (el: HTMLDivElement) => {
        if (el && !itemsRef.current.includes(el)) {
            itemsRef.current.push(el);
        }
    };

    useLayoutEffect(() => {
        ScrollTrigger.saveStyles(itemsRef.current);
        const ctx = gsap.context(() => {
            const startOffset = 220; //adjust speed
            const finishOffset = 8; //adjust spacing between elements

            // Kill previous animations before creating new ones
            gsap.killTweensOf(itemsRef.current);
            ScrollTrigger.getAll().forEach((st) => st.kill());

            const tl = gsap.timeline({
                scrollTrigger: {
                    trigger: triggerRef.current,
                    start: 'top top',
                    end: '2000 top', //another way to adjust speed by making the user scroll more
                    scrub: 0.6,
                    pin: true,
                    toggleActions: 'play none none reverse',
                },
            });

            itemsRef.current.forEach((item, i) => {
                tl.fromTo(
                    item,
                    { x: `${startOffset + i * 60}vh`, opacity: 0 },
                    {
                        x: `${finishOffset + i * 5}rem`,
                        opacity: 1,
                        ease: 'none',
                        duration: 100,
                    },
                    '+=0.5', // Delay between animations
                );
            });
        });

        return () => {
            ctx.revert(); // Cleanup GSAP context
        };
    }, []);

    return (
        <Fragment>
            {isDesktop ? (
                <div className="w-full relative">
                    {/* Sticky Title */}
                    <div className="sticky xl:h-[60rem] md:h-[50rem] h-[48rem]  top-0 z-50 pt-[6rem] md:pt-[6rem] ml-[9%] bg-transparent">
                        <div className="sm:text-4xl text-3xl sm:mb-20 mb-10 flex items-center space-x-4 p-4">
                            <img src="./JourneySection/symbol.svg" alt="" className="w-[1.6rem]" />
                            <p className="text-white tracking-[0.2em]">JOURNEY</p>
                        </div>
                    </div>

                    {/* Animated Section */}
                    <section className="scroll-section-outer mt-[10rem] mr-20 gap-[20rem] min-h-[40rem]">
                        <div ref={triggerRef} className="mr-0 relative w-full h-screen">
                            {journeyEntries.map((entry, index) => (
                                <div
                                    key={index}
                                    ref={addToRefs}
                                    className="absolute top-0 left-0 w-full"
                                    style={{ zIndex: index + 1 }}
                                >
                                    <DesktopJourneyModule title={entry.title} text={entry.text} />
                                </div>
                            ))}
                            <div
                                ref={addToRefs}
                                className="absolute top-0 left-0 w-full"
                                style={{ zIndex: 0, display: 'none' }}
                            ></div>
                        </div>
                    </section>
                </div>
            ) : (
                <div className="w-full relative">
                    <div className="pt-[6rem] md:pt-[6rem] ml-[9%] bg-transparent">
                        <div className="sm:text-4xl text-3xl sm:mb-20 mb-10 flex items-center space-x-4 p-4">
                            <img src="./JourneySection/symbol.svg" alt="" className="w-[1.6rem]" />
                            <p className="text-white tracking-[0.2em]">JOURNEY</p>
                        </div>
                    </div>

                    <section className=" min-h-[40rem] relative w-full">
                        <div className="relative w-full flex flex-col gap-[5rem] object-center">
                            {journeyEntries.map((entry, index) => (
                                <div key={index} className="w-full" style={{ zIndex: index + 1 }}>
                                    <MobileJourneyModule title={entry.title} text={entry.text} />
                                </div>
                            ))}
                        </div>
                    </section>
                </div>
            )}
        </Fragment>
    );
}

export default JourneySection;
