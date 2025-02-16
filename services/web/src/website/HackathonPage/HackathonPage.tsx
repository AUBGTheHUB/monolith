import { Fragment } from 'react/jsx-runtime';
import { Footer } from './Footer/HackathonFooter';
import ScheduleSection from './ScheduleSection/ScheduleSection';
import { Recap } from './components/Recap';
import JourneySection from './JourneySection/JourneySection';

export const HackathonPage = () => {
    return (
        <Fragment>
            <JourneySection/>
            <ScheduleSection />
            <Recap />
            <Footer />
        </Fragment>
    );
};
