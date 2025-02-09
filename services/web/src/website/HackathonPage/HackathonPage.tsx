import { Fragment } from 'react/jsx-runtime';

import { DesktopNavComponent } from './Navigation/DesktopNav';
import ScheduleSection from './ScheduleSection/ScheduleSection';

export const HackathonPage = () => {
    return (
        <Fragment>
            <DesktopNavComponent />
            <h1>HackPage</h1>
            <h1 className="font-distant text-white">SF Distant Galaxy Regular</h1>
            <ScheduleSection />
        </Fragment>
    );
};
