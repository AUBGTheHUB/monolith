import { Fragment } from 'react/jsx-runtime';
import JurySection from './CarouselComponents/components/JurySection/components/JurySection';
import MentorsSection from './CarouselComponents/components/MentorsSection/components/MentorsSection';

import { Navigation } from './Navigation/Navigation';
import { Footer } from './Footer/HackathonFooter';
import ScheduleSection from './ScheduleSection/ScheduleSection';
import AwardsSection from './AwardsSection/AwardsSection';
import { Recap } from './components/Recap';

export const HackathonPage = () => {
    return (
        <Fragment>
            <Navigation />
            <MentorsSection></MentorsSection>
            <JurySection></JurySection>
            <ScheduleSection />
            <Recap />
            <AwardsSection />
            <Footer />
        </Fragment>
    );
};
