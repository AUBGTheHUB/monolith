import { JourneyDesktop } from './JourneyDesktop/JourneyDesktop';
import { useMediaQuery } from 'react-responsive';

export const NavBar = ({ props }) => {
    const isMobile = useMediaQuery({ query: '(max-width: 900px)' });

    if (!isMobile) {
        return <JourneyDesktop props={props} />;
    } else {
        return <p>lool</p>;
    }
};
