import { Fragment } from 'react/jsx-runtime';
import JurySection from './CarouselComponents/components/JurySection/components/JurySection';
import MentorsSection from './CarouselComponents/components/MentorsSection/components/MentorsSection';
import { Navigation } from './Navigation/Navigation';
import { Footer } from './Footer/HackathonFooter';
import GradingSection from './GradingSection/GradingSection';
import ScheduleSection from './ScheduleSection/ScheduleSection';
import LandingSection from './LandingSection/LandingSection';
import MissionSection from './MissionSection/MissionSection';
import AwardsSection from './AwardsSection/AwardsSection';
import { Recap } from './components/Recap';
import { useFeatureSwitches } from '@/config';
import HackathonFAQSection from './FAQSection/HackathonFAQ';
import HackathonSponsors from './SponsorsSection/HackathonSponsors';

export const HackathonPage = () => {
    const featureSwitches = useFeatureSwitches();

    return (
        <Fragment>
            <Navigation />
            <div className="relative">
                <LandingSection />
                <MissionSection />
            </div>
            <MentorsSection mentorsSwitch={featureSwitches.MentorsSwitch} />
            <JurySection jurySwitch={featureSwitches.JurySwitch} />
            <ScheduleSection />
            <Recap />
            <GradingSection />
            <AwardsSection />
            <HackathonSponsors />
            <HackathonFAQSection />
            <Footer />
        </Fragment>
    );
};
