import { Fragment } from 'react/jsx-runtime';
import JurySection from './CarouselComponents/components/JurySection/components/JurySection';
import MentorsSection from './CarouselComponents/components/MentorsSection/components/MentorsSection';
import ScheduleSection from './ScheduleSection/ScheduleSection';

export const HackathonPage = () => {
    return (
        <Fragment>
            <h1 className="font-distant text-white">SF Distant Galaxy Regular</h1>
            <MentorsSection></MentorsSection>
            <JurySection></JurySection>
            <ScheduleSection />
        </Fragment>
    );
};
