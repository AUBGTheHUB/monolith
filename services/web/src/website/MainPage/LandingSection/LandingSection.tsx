import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Navigation } from '../Navigation/Navigation';

export default function LandingSection() {
    const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
    const [isHovered, setIsHovered] = useState(() => window.innerWidth < 640);

    const handleMouseMove = (e: React.MouseEvent) => {
        const rect = e.currentTarget.getBoundingClientRect();
        setMousePosition({
            x: e.clientX - rect.left,
            y: e.clientY - rect.top,
        });
    };

    return (
        <div
            className="relative overflow-hidden h-[100vh] select-none scroll-smooth"
            onMouseMove={handleMouseMove}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
        >
            <img
                src="/landingSection/circuit.png"
                alt="Circuit board"
                className={`absolute w-full h-full object-cover sm:opacity-30 opacity-5`}
                style={{
                    opacity: isHovered ? (window.innerWidth >= 640 ? 0.3 : 0.05) : 0,
                    transition: 'opacity 0ms ease-in-out',
                    WebkitMaskImage:
                        window.innerWidth >= 640 && isHovered
                            ? `radial-gradient(circle at ${mousePosition.x}px ${mousePosition.y}px, rgba(0, 0, 0, 1) 75px, rgba(0, 0, 0, 0) 150px)`
                            : 'none',
                    maskImage:
                        window.innerWidth >= 640 && isHovered
                            ? `radial-gradient(circle at ${mousePosition.x}px ${mousePosition.y}px, rgba(0, 0, 0, 1) 75px, rgba(0, 0, 0, 0) 150px)`
                            : 'none',
                    WebkitMaskRepeat: 'no-repeat',
                    maskRepeat: 'no-repeat',
                }}
            />
            <img
                src="/landingSection/blob-blue.png"
                alt="a blob"
                className="absolute hidden sm:block opacity-65 blur-[10rem] h-[93rem] right-[0rem] z-0"
            />
            <img
                src="/landingSection/blob-cyan.png"
                alt="a blob"
                className="absolute hidden sm:block opacity-65 blur-[10rem] h-[53rem] w-[56rem] right-[-8rem] top-[30rem] z-0"
            />
            <div className="flex flex-col bg-transparent h-[100vh]">
                <Navigation />
                <div className="flex items-center justify-center font-mont z-10 h-[80%]">
                    <div className="sm:w-2/5 w-11/12">
                        <div className="flex flex-col items-center text-center">
                            <div>
                                <p className="text-2xl text-[#9CBEFF] mb-[10px]">WELCOME TO</p>
                                <h1 className="text-7xl sm:text-8xl font-bold bg-gradient-to-b from-[#FFFFFF] to-[#33C8FF] bg-clip-text text-transparent">
                                    THE HUB
                                </h1>
                                <p className="text-base text-white mt-[18px] mb-[30px]">
                                    A group of passionate IT-oriented students who strive to make technological
                                    innovation thrive within AUBG and beyond.
                                </p>
                            </div>
                            <div className="flex space-x-4">
                                <Button
                                    className="border-[1px] border-white text-white bg-transparent rounded-3xl
                   sm:hover:bg-white sm:hover:text-[#26368E]
                   sm:transition sm:duration-300 sm:ease-in-out"
                                >
                                    Find out more
                                </Button>
                                <Button
                                    className="border-[1px] border-white text-white bg-transparent rounded-3xl
                   sm:hover:bg-white sm:hover:text-[#26368E]
                   sm:transition sm:duration-300 sm:ease-in-out"
                                >
                                    Contact us
                                </Button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
