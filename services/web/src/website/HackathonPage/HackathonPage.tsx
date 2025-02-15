import { Fragment } from 'react/jsx-runtime';
import ScheduleSection from './ScheduleSection/ScheduleSection';
import LandingSection from './LandingSection/LandingSection';
import MissionSection from './MissionSection/MissionSection';

export const HackathonPage = () => {
    return (
        <Fragment>
            <div className="relative">
                <LandingSection />
                <MissionSection />
            </div>
            <ScheduleSection />
        </Fragment>
    );
};
