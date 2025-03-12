import { useEffect, useState } from 'react';
import logo from './images/hublogo.webp';

export const DesktopNavComponent = () => {
    const NAV_ITEM_A = 'text-white font-light font-mont';
    const NAV_ITEM_A_EFFECT =
        'hover:text-white relative after:content-[""] after:absolute after:w-full after:scale-x-0 after:h-[2px] after:bottom-[-4px] after:left-0 after:bg-white after:origin-bottom-right after:transition-transform after:duration-300 hover:after:scale-x-100 hover:after:origin-bottom-left';
    const [fadeIn, setFadeIn] = useState(false);
    useEffect(() => {
        const timer = setTimeout(() => {
            setFadeIn(true);
        }, 400);

        return () => clearTimeout(timer);
    }, []);

    return (
        <div
            className={`w-full h-[10%] bg-[rgba(0,0,0,0.5)] border-gray-600 py-2 sticky top-0 z-[100]  transform transition-all duration-1000 ease-in-out ${fadeIn ? 'opacity-100' : 'opacity-0'}`}
        >
            <div className="w-full flex flex-row justify-center items-center">
                <div className="w-[8%] items-center z-10 flex justify-center">
                    <a href="/" className="cursor-pointer ">
                        <img src={logo} className="h-[50px] my-[15px]" />
                    </a>
                </div>
                <div className="flex flex-row w-[70%] gap-7">
                    <a href="#mission" className={`${NAV_ITEM_A} ${NAV_ITEM_A_EFFECT}`}>
                        About
                    </a>
                    <a href="#schedule" className={`${NAV_ITEM_A} ${NAV_ITEM_A_EFFECT}`}>
                        Schedule
                    </a>
                    <a href="#grading-criteria" className={`${NAV_ITEM_A} ${NAV_ITEM_A_EFFECT}`}>
                        Grading Criteria
                    </a>
                    <a href="#faq" className={`${NAV_ITEM_A} ${NAV_ITEM_A_EFFECT}`}>
                        FAQ
                    </a>
                </div>
                <div>
                    <a
                        href="/hackathon/registration"
                        className={`${NAV_ITEM_A} border-2 border-sky-600 rounded-3xl px-4 py-1 hover:text-white hover:bg-sky-600 transition-colors duration-500`}
                    >
                        Participate now
                    </a>
                </div>
            </div>
        </div>
    );
};
