import { useEffect, useState } from 'react';
import MissionSection from '../MissionSection/MissionSection';

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
            className={`
                            transform transition-all duration-1000 ease-in-out
                            ${fadeIn ? 'opacity-100' : 'opacity-0'}
                            `}
        >
            <div
                className=" w-full h-auto lg:pb-[55rem] max-[1024px]:min-h-[100vh] pb-[55rem] relative"
                style={{
                    backgroundImage: 'url("/verifyPage/background.png")',
                    backgroundSize: 'cover',
                    backgroundPosition: 'right',
                    backgroundRepeat: 'repeat',
                }}
            >
                <img
                    className="lg:w-[40%] absolute z-10 lg:top-0 right-0 top-[25rem] w-[70%]"
                    src="/hackLanding/death_star.svg"
                />
                <div className="w-full flex justify-center  min-h-[100vh] lg:min-h-[80vh]">
                    <div className="flex justify-center max-[1024px]:items-start max-[1024px]:mt-[5rem] w-full">
                        <img className="flex z-50 lg:w-1/2 w-[90%]" src="/hackLanding/title.svg" />
                    </div>
                </div>
                <MissionSection />
            </div>
        </div>
    );
}
