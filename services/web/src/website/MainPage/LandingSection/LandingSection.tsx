import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Navigation } from '../Navigation/Navigation';
import { useTypewriter, Cursor } from 'react-simple-typewriter';

export default function LandingSection() {
    const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
    const [isHovered, setIsHovered] = useState(() => window.innerWidth < 640);

    const [fadeIn, setFadeIn] = useState(false);

    const [heading] = useTypewriter({
        words: ['THE HUB'],
        loop: 15,
        typeSpeed: 80,
        deleteSpeed: 100,
        delaySpeed: 7000,
    });

    useEffect(() => {
        const timer = setTimeout(() => {
            setFadeIn(true);
        }, 400);

        return () => clearTimeout(timer);
    }, []);

    const handleMouseMove = (e: React.MouseEvent) => {
        const rect = e.currentTarget.getBoundingClientRect();
        setMousePosition({
            x: e.clientX - rect.left,
            y: e.clientY - rect.top,
        });
    };

    return (
        <div
            className="relative overflow-hidden h-[100vh] select-none"
            onMouseMove={handleMouseMove}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
        >
            <img
                src="/landingSection/circuit.webp"
                alt="Circuit board"
                className="absolute w-full h-full object-cover sm:opacity-30 opacity-5"
                style={{
                    opacity: isHovered ? (window.innerWidth >= 640 ? 0.3 : 0.05) : 0,
                    transition: 'opacity 0ms ease-in-out',
                    WebkitMaskImage:
                        window.innerWidth >= 640 && isHovered
                            ? `radial-gradient(circle at ${mousePosition.x}px ${mousePosition.y}px, rgba(0,0,0,1) 75px, rgba(0,0,0,0) 150px)`
                            : 'none',
                    maskImage:
                        window.innerWidth >= 640 && isHovered
                            ? `radial-gradient(circle at ${mousePosition.x}px ${mousePosition.y}px, rgba(0,0,0,1) 75px, rgba(0,0,0,0) 150px)`
                            : 'none',
                    WebkitMaskRepeat: 'no-repeat',
                    maskRepeat: 'no-repeat',
                }}
            />

            <img
                src="https://hubarskibucket.s3.eu-central-1.amazonaws.com/the-hub-2025/website-elements/gradient-top.webp"
                alt="a gradient"
                className="absolute hidden pointer-events-none sm:block h-[163rem] w-full right-[0-rem] z-0"
            />
            <div
                className={`
                            transform transition-all duration-1000 ease-in-out
                            ${fadeIn ? 'opacity-100' : 'opacity-0'}
                            `}
            >
                <div className="flex flex-col bg-transparent h-[100vh]">
                    <Navigation />
                    <div className="flex items-center justify-center font-mont z-10 h-[80%]">
                        <div className="sm:w-11/12 xl:w-2/5 w-11/12">
                            <div className="flex flex-col items-center justify-center">
                                <p className="text-2xl text-[#9CBEFF] mb-[10px]">WELCOME TO</p>
                                <h1 className="relative text-7xl sm:text-8xl font-bold bg-gradient-to-b from-[#FFFFFF] to-[#33C8FF] bg-clip-text text-transparent md:min-h-[96px] min-h-[72px] text-center">
                                    {heading}
                                    <Cursor
                                        cursorBlinking
                                        cursorStyle={
                                            <span className="absolute bg-gradient-to-b from-[#FFFFFF] to-[#33C8FF] w-[8px] h-[65%] bottom-[15%] ml-[10px]" />
                                        }
                                    />
                                </h1>
                                <p className="text-base md:text-[1.125rem] text-center text-white mt-[18px] mb-[30px]">
                                    A group of passionate IT-oriented students who strive to make technological
                                    innovation thrive within AUBG and beyond.
                                </p>
                            </div>
                            <div className="flex justify-center space-x-4">
                                <a href="#about-us">
                                    <Button
                                        className="border-[1px] border-white text-white bg-transparent rounded-3xl
                                        sm:hover:bg-white sm:hover:text-[#26368E]
                                        sm:transition sm:duration-300 sm:ease-in-out"
                                    >
                                        Find out more
                                    </Button>
                                </a>
                                <a href="#footer">
                                    <Button
                                        className="border-[1px] border-white text-white bg-transparent rounded-3xl
                                        sm:hover:bg-white sm:hover:text-[#26368E]
                                        sm:transition sm:duration-300 sm:ease-in-out"
                                    >
                                        Contact us
                                    </Button>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
