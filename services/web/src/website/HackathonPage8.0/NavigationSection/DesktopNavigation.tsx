import { useEffect, useState } from 'react';

export const DesktopNavigationComponent = () => {
    const NAV_ITEM_A = 'text-[rgba(255,253,245,1)] text-xs font-thin font-orbitron';
    const NAV_ITEM_A_EFFECT =
        'hover:text-[rgba(255,253,245,1)] relative after:content-[""] after:absolute after:w-full after:scale-x-0 after:h-[2px] after:bottom-[-4px] after:left-0 after:bg-[rgba(255,253,245,1)] after:origin-bottom-right after:transition-transform after:duration-300 hover:after:scale-x-100 hover:after:origin-bottom-left';
    const [fadeIn, setFadeIn] = useState(false);
    useEffect(() => {
        const timer = setTimeout(() => {
            setFadeIn(true);
        }, 400);

        return () => clearTimeout(timer);
    }, []);

    return (
        <div className="p-4">
            <div
                className={`rounded-2xl px-6 bg-[rgba(28,26,25,0.9)] border-gray-600 py-2 sticky top-0 z-[100]  transform transition-all duration-1000 ease-in-out ${fadeIn ? 'opacity-100' : 'opacity-0'}`}
            >
                <div className="w-full flex flex-row justify-center items-center py-3">
                    <div className="flex flex-row w-[85%] gap-8">
                        <a href="#about" className={`${NAV_ITEM_A} ${NAV_ITEM_A_EFFECT}`}>
                            ABOUT
                        </a>
                        <a href="#schedule" className={`${NAV_ITEM_A} ${NAV_ITEM_A_EFFECT}`}>
                            SCHEDULE
                        </a>
                        <a href="#journey" className={`${NAV_ITEM_A} ${NAV_ITEM_A_EFFECT}`}>
                            JOURNEY
                        </a>
                        <a href="#grading-criteria" className={`${NAV_ITEM_A} ${NAV_ITEM_A_EFFECT}`}>
                            GRADING CRITERIA
                        </a>
                        <a href="#faq" className={`${NAV_ITEM_A} ${NAV_ITEM_A_EFFECT}`}>
                            FAQ
                        </a>
                    </div>
                    <div>
                        <a href="/hackathon/registration" className={`${NAV_ITEM_A} text-center  hover:text-white`}>
                            PARTICIPATE NOW
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
};
