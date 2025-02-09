import { Fragment } from 'react/jsx-runtime';
import ScheduleSection from './ScheduleSection/ScheduleSection';
import AwardsSection from './AwardsSection/AwardsSection';

export const HackathonPage = () => {
    return (
        <Fragment>
            <h1 className="font-distant text-white">SF Distant Galaxy Regular</h1>
            <ScheduleSection />
            <AwardsSection />
        </Fragment>
    );
};
