import { JourneyDesktop } from './JourneyDesktop/JourneyDesktop';
import { JourneyMobile } from './JourneyMobile/JourneyMobile';
import { useMediaQuery } from 'react-responsive';

export const JourneySection = ({ props }) => {
    const isMobile = useMediaQuery({ query: '(max-width: 900px)' });

    if (!isMobile) {
        return <JourneyDesktop props={props} />;
    } else {
        return <JourneyMobile props={props} />;
    }
};
