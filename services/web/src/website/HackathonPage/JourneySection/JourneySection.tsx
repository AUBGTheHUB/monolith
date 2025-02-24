import React, { useRef, useEffect } from 'react';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/dist/ScrollTrigger';
import JourneyModule from './JourneyModule';
import journeyEntries from './StaticContent/journeyEntries.json';

function JourneySection() {
    //const sectionRef = useRef(null);
    const triggerRef = useRef(null);

    const itemsRef = useRef<HTMLDivElement[]>([]);

    const startOffset = window.innerWidth <= 768 ? 50 : 220;

    const finishOffset = window.innerWidth <= 768 ? 4 : 8;

    // Helper to add each element to the ref array
    const addToRefs = (el: HTMLDivElement) => {
        if (el && !itemsRef.current.includes(el)) {
            itemsRef.current.push(el);
        }
    };

    gsap.registerPlugin(ScrollTrigger);

    useEffect(() => {
        const pin = gsap.fromTo(
            itemsRef.current,
            {
                // Start off-screen to the right (adjust value as needed)
                x: (i: number) => `${startOffset + i * 60}vh`,
            },
            {
                // Animate each element to x = 0 (the left edge of its container)
                x: (i: number) => `${window.innerWidth <= 768 ? finishOffset : finishOffset + i * 5}rem`,
                ease: 'none',
                duration: 1,
                // Animate one after the other so they appear to stack as they slide in
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
        return () => {
            // Cleanup the animation on component unmount
            pin.kill();
        };
    }, []);

    return (
        <div className="w-full relative">
            <div className="sticky h-[50rem] top-0 z-50 p-4 ml-[9%] bg-transparent">
                <div className="sm:text-4xl text-3xl sm:mb-20 mb-10 flex items-center space-x-4 p-4">
                    <img src="./JourneySection/symbol.svg" alt="" className="w-[1.6rem]" />
                    <p className="text-white tracking-[0.2em]">JOURNEY</p>
                </div>
            </div>
            <section className="scroll-section-outer mr-20 gap-[20rem] min-h-[40rem]">
                <div ref={triggerRef} className="mr-0 relative w-full h-screen ">
                    {journeyEntries.map((entry, index) => {
                        return (
                            <div
                                key={index}
                                ref={addToRefs}
                                className="absolute top-0 left-0 w-full"
                                // Increase z-index for later items so they appear on top
                                style={{ zIndex: index + 1 }}
                            >
                                <JourneyModule title={entry.title} text={entry.text} />
                            </div>
                        );
                    })}
                </div>
                {/* Repeat similar blocks for other content sections... */}
            </section>
        </div>
    );
}

export default JourneySection;
