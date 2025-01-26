import { useState, useEffect, Fragment } from 'react';
import DesktopNavComponent from './DesktopNav.tsx';
import MobileNavComponent from './MobileNav.tsx';

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

    return <Fragment>{isDesktop ? <DesktopNavComponent /> : <MobileNavComponent />}</Fragment>;
};
