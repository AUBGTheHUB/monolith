import { useState, useEffect } from 'react';
import { DesktopNavComponent } from './DesktopNav.tsx';
import { MobileNavComponent } from './MobileNav.tsx';

export const Navigation = () => {
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
            {isDesktop ? <DesktopNavComponent /> : <MobileNavComponent />}
        </div>
    );
};
