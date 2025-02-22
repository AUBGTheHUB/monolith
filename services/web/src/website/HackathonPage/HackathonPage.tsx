import { Fragment } from 'react/jsx-runtime';
import { Navigation } from './Navigation/Navigation';
import { Footer } from './Footer/HackathonFooter';
import GradingSection from './GradingSection/GradingSection';
import ScheduleSection from './ScheduleSection/ScheduleSection';
import AwardsSection from './AwardsSection/AwardsSection';
import { Recap } from './components/Recap';

export const HackathonPage = () => {
    return (
        <Fragment>
            <Navigation />
            <ScheduleSection />
            <Recap />
            <GradingSection />
            <AwardsSection />
            <Footer />
        </Fragment>
    );
};
