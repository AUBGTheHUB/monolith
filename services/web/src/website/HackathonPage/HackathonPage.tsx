import { Fragment } from 'react/jsx-runtime';

import { Navigation } from './Navigation/Navigation';
import ScheduleSection from './ScheduleSection/ScheduleSection';

export const HackathonPage = () => {
    return (
        <Fragment>
            <Navigation />
            <ScheduleSection />
        </Fragment>
    );
};
