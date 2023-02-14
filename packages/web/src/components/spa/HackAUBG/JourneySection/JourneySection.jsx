import { JourneyDesktop } from './JourneyDesktop/JourneyDesktop';
import { JourneyMobile } from './JourneyMobile/JourneyMobile';
import { useMediaQuery } from 'react-responsive';

export const JourneySection = ({ props }) => {
    const isMobile = useMediaQuery({ query: '(max-width: 1200px)' });

    if (!isMobile) {
        return <JourneyDesktop props={props} />;
    } else {
        return <JourneyMobile props={props} />;
    }
};
