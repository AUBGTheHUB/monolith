import { Fragment } from 'react/jsx-runtime';
import { Footer } from './Footer/HackathonFooter';
import ScheduleSection from './ScheduleSection/ScheduleSection';
import { Recap } from './components/Recap';

export const HackathonPage = () => {
    return (
        <Fragment>
            <ScheduleSection />
            <Recap />
            <Footer />
        </Fragment>
    );
};
