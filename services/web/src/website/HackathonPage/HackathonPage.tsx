import { Fragment } from 'react/jsx-runtime';

import { Navigation } from './Navigation/Navigation';
import { Footer } from './Footer/HackathonFooter';
import ScheduleSection from './ScheduleSection/ScheduleSection';
import LandingSection from './LandingSection/LandingSection';
import MissionSection from './MissionSection/MissionSection';
import AwardsSection from './AwardsSection/AwardsSection';
import { Recap } from './components/Recap';

export const HackathonPage = () => {
    return (
        <Fragment>
            <Navigation />
            <div className="relative">
                <LandingSection />
                <MissionSection />
            </div>
            <ScheduleSection />
            <Recap />
            <AwardsSection />
            <Footer />
        </Fragment>
    );
};
