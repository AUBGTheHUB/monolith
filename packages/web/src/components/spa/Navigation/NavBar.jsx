import { NavDesktop } from './DesktopNav/NavDesktop';
import { NavMobile } from './MobileNav/NavMobile';
import { useMediaQuery } from 'react-responsive';

export const NavBar = ({ props }) => {
    const isMobile = useMediaQuery({ query: '(max-width: 900px)' });

    if (!isMobile) {
        return <NavDesktop props={props} />;
    } else {
        return <NavMobile props={props} />;
    }
};
