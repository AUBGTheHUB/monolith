import { Fragment } from 'react/jsx-runtime';

import { Navigation } from './Navigation/Navigation';
import { Footer } from './Footer/HackathonFooter';
import ScheduleSection from './ScheduleSection/ScheduleSection';
import { Recap } from './components/Recap';
import JourneySection from './JourneySection/JourneySection';
import ScrollSection from './JourneySection/scrollingsection';

export const HackathonPage = () => {
    return (
        <Fragment>
            <JourneySection/>
            <ScheduleSection />
            <Recap />
            <JourneySection/>
            <Footer />
        </Fragment>
    );
};
