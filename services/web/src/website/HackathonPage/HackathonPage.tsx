import JurySection from './CarouselComponents/components/JurySection/components/JurySection';
import MentorsSection from './CarouselComponents/components/MentorsSection/components/MentorsSection';
import { Navigation } from './NavigationSection/Navigation';
import { Footer } from './FooterSection/HackathonFooter';
import GradingSection from './GradingSection/GradingSection';
import ScheduleSection from './ScheduleSection/ScheduleSection';
import LandingSection from './LandingSection/LandingSection';
import AwardsSection from './AwardsSection/AwardsSection';
import { Recap } from './RecapSection/Recap';
import { useFeatureSwitches } from '@/config';
import JourneySection from './JourneySection/JourneySection';
import HackathonFAQSection from './FAQSection/HackathonFAQ';
import HackathonSponsors from './SponsorsSection/HackathonSponsors';
import { Helmet } from 'react-helmet';

export const HackathonPage = () => {
    const featureSwitches = useFeatureSwitches();

    return (
        <div className="bg-[#000a12]">
            <Helmet>
                <title>Hackathon 7.0</title>
                <link rel="icon" href="faviconHack.ico" />
            </Helmet>
            <Navigation />
            <LandingSection />
            <JourneySection />
            <MentorsSection mentorsSwitch={featureSwitches.MentorsSwitch} />
            <JurySection jurySwitch={featureSwitches.JurySwitch} />
            <ScheduleSection />
            <Recap />
            <GradingSection />
            <AwardsSection />
            <HackathonSponsors sponsorsSwitch={featureSwitches.SponsorsSwitch} />
            <HackathonFAQSection />
            <Footer />
        </div>
    );
};
