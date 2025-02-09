import { Fragment } from 'react/jsx-runtime';
import { Footer } from './Footer/footer';
import ScheduleSection from './ScheduleSection/ScheduleSection';

export const HackathonPage = () => {
    return (
        <Fragment>
            <h1 className="font-distant text-white">SF Distant Galaxy Regular</h1>
            <ScheduleSection />
            <Footer />
        </Fragment>
    );
};
