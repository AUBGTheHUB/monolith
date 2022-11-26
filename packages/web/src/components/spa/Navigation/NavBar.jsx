import { NavDesktop } from './DesktopNav/NavDesktop';
import { NavMobile } from './MobileNav/NavMobile';
import { useMediaQuery } from 'react-responsive';

export const NavBar = () => {
    const isDesktop = useMediaQuery({ query: '(max-width: 1000px)' });

    if (!isDesktop) {
        return <NavDesktop />;
    } else {
        return <NavMobile />;
    }
};
