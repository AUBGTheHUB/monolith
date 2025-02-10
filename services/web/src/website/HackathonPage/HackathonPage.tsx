import { Fragment } from 'react/jsx-runtime';
import GradingSection from './GradingSection/GradingSection';
import ScheduleSection from './ScheduleSection/ScheduleSection';

export const HackathonPage = () => {
    return (
        <Fragment>
            <h1 className="font-distant text-white">SF Distant Galaxy Regular</h1>
            <ScheduleSection />
            <GradingSection />
        </Fragment>
    );
};
