import { useEffect, useState } from 'react';
import { CornerUpLeft } from 'lucide-react';

export const DesktopNavComponent = () => {
    const [fadeIn, setFadeIn] = useState(false);
    useEffect(() => {
        const timer = setTimeout(() => {
            setFadeIn(true);
        }, 400);

        return () => clearTimeout(timer);
    }, []);

    return (
        <div className="p-4 fixed top-3 right-3 z-[100]">
            <a
                href="/hackathon"
                className={`inline-flex items-center gap-2 rounded-full px-6 py-3 bg-[rgba(0,0,0,0.5)] border border-gray-600 text-white text-sm font-light font-mont tracking-wider hover:text-white hover:bg-[rgba(0,0,0,0.7)] hover:border-gray-400 transition-all duration-300 transform relative after:content-[""] after:absolute after:w-[calc(100%-3rem)] after:scale-x-0 after:h-[1px] after:bottom-2.5 after:left-6 after:bg-white after:origin-bottom-right after:transition-transform after:duration-300 hover:after:scale-x-100 hover:after:origin-bottom-left ${fadeIn ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-2'}`}
            >
                <CornerUpLeft size={16} strokeWidth={1.5} />
                Go back
            </a>
        </div>
    );
};
