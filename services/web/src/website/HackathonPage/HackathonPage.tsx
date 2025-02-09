import { Fragment } from 'react/jsx-runtime';

import { Navigation } from './Navigation/Navigation';
import ScheduleSection from './ScheduleSection/ScheduleSection';

export const HackathonPage = () => {
    return (
        <Fragment>
            <Navigation />
            <h1 className="font-distant text-white">SF Distant Galaxy Regular</h1>
            <ScheduleSection />
        </Fragment>
    );
};
