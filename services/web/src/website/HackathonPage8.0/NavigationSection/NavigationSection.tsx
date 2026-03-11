import { useState, useEffect, Fragment } from 'react';
import { DesktopNavigationComponent } from './DesktopNavigation.tsx';
import { MobileNavigationComponent } from './MobileNavigation.tsx';

export const NavigationSection = () => {
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

    return <Fragment>{isDesktop ? <DesktopNavigationComponent /> : <MobileNavigationComponent />}</Fragment>;
};
