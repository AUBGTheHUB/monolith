import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Navigation } from '../Navigation/Navigation';

export default function LandingSection() {
    const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

    const handleMouseMove = (e: React.MouseEvent) => {
        const rect = e.currentTarget.getBoundingClientRect();
        setMousePosition({
            x: e.clientX - rect.left,
            y: e.clientY - rect.top,
        });
    };

    return (
        <div className="relative overflow-hidden h-[100vh] select-none" onMouseMove={handleMouseMove}>
            <img
                src="/landingSection/circuit.png"
                alt="Circuit board"
                className={`absolute w-full h-full object-cover sm:opacity-30 opacity-15 `}
                style={{
                    WebkitMaskImage:
                        window.innerWidth >= 640
                            ? `radial-gradient(circle at ${mousePosition.x}px ${mousePosition.y}px, rgba(0, 0, 0, 1) 112.5px, rgba(0, 0, 0, 0) 225px)`
                            : 'none',
                    maskImage:
                        window.innerWidth >= 640
                            ? `radial-gradient(circle at ${mousePosition.x}px ${mousePosition.y}px, rgba(0, 0, 0, 1) 112.5px, rgba(0, 0, 0, 0) 225px)`
                            : 'none',
                    WebkitMaskRepeat: 'no-repeat',
                    maskRepeat: 'no-repeat',
                }}
            />
            <img
                src="/landingSection/blob-blue.png"
                alt="a blob"
                className="absolute opacity-65 blur-[10rem] h-[1490.43px] right-[0rem] z-0"
            />
            <img
                src="/landingSection/blob-cyan.png"
                alt="a blob"
                className="absolute opacity-65 blur-[10rem] h-[852.29px] w-[895.03px] right-[-8vh] top-[30vh] z-0"
            />
            <div className="flex flex-col bg-[#0b1224] h-[100vh]">
                <Navigation />
                <div className="flex items-center justify-center font-mont z-10 h-[80%]">
                    <div className="sm:w-2/5 w-11/12">
                        <div className="flex flex-col items-center text-center space-y-6">
                            <div>
                                <p className="text-2xl text-blue-200">WELCOME TO</p>
                                <p className="text-7xl sm:text-8xl  font-bold bg-gradient-to-b from-[#FFFFFF] to-[#33C8FF] bg-clip-text text-transparent">
                                    THE HUB
                                </p>
                                <p className="text-base  text-white">
                                    A group of passionate IT-oriented students who strive to make technological
                                    innovation thrive within AUBG and beyond.
                                </p>
                            </div>
                            <div className="flex space-x-4">
                                <Button
                                    className="border-[0.5px] border-white text-white bg-transparent rounded-3xl 
                   sm:hover:bg-white sm:hover:text-blue-950
                   sm:transition sm:duration-300 sm:ease-in-out"
                                >
                                    Find out more
                                </Button>
                                <Button
                                    className="border-[0.5px] border-white text-white bg-transparent rounded-3xl 
                   sm:hover:bg-white sm:hover:text-blue-950
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
