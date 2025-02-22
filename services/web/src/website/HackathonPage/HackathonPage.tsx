import { Fragment } from 'react/jsx-runtime';
import JurySection from './CarouselComponents/components/JurySection/components/JurySection';
import MentorsSection from './CarouselComponents/components/MentorsSection/components/MentorsSection';
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
            <MentorsSection />
            <JurySection />
            <ScheduleSection />
            <Recap />
            <GradingSection />
            <AwardsSection />
            <Footer />
        </Fragment>
    );
};
