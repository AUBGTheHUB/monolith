import { Fragment } from 'react/jsx-runtime';

import { Navigation } from './Navigation/Navigation';
import { Footer } from './Footer/HackathonFooter';
import ScheduleSection from './ScheduleSection/ScheduleSection';
import { Recap } from './components/Recap';

export const HackathonPage = () => {
    return (
        <Fragment>
            <Navigation />
            <ScheduleSection />
            <Recap />
            <Footer />
        </Fragment>
    );
};
