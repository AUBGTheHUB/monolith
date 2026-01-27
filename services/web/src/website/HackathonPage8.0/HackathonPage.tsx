import { Helmet } from 'react-helmet';
import { AwardsSection } from './AwardsSection/AwardsSection';
import { FAQSection } from './FAQSection/FAQSection';
import { FooterSection } from './FooterSection/FooterSection';
import { GradingSection } from './GradingSection/GradingSection';
import { JourneySection } from './JourneySection/JourneySection';
import { LandingSection } from './LandingSection/LandingSection';
import { MentorsAndJudgesSection } from './MentorsAndJudgesSection/MentorsAndJudgesSection';
import { MissionSection } from './MissionSection/MissionSection';
import { NavigationSection } from './NavigationSection/NavigationSection';
import { RecapSection } from './RecapSection/RecapSection';
import { ScheduleSection } from './ScheduleSection/ScheduleSection';
import { SponsorsSection } from './SponsorsSection/SponsorsSection';

export const HackathonPage = () => {
    return (
        <div className="bg-[#000a12]">
            <Helmet>
                <title>Hackathon 7.0</title>
                <link rel="icon" href="/faviconHack.ico" />
                <NavigationSection />
                <LandingSection />
                <MissionSection />
                <JourneySection />
                <MentorsAndJudgesSection />
                <ScheduleSection />
                <RecapSection />
                <GradingSection />
                <AwardsSection />
                <SponsorsSection />
                <FAQSection />
                <FooterSection />
            </Helmet>
        </div>
    );
};
