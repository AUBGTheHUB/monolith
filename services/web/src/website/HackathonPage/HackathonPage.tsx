import { Fragment } from 'react/jsx-runtime';

import { Navigation } from './Navigation/Navigation';
import { Footer } from './Footer/HackathonFooter';
import ScheduleSection from './ScheduleSection/ScheduleSection';
import { Recap } from './components/Recap';
import JourneySection from './JourneySection/JourneySection';

export const HackathonPage = () => {
    return (
        <Fragment>
            <Navigation />
            <JourneySection/>
            <ScheduleSection />
            <Recap />
            <Footer />
        </Fragment>
    );
};
