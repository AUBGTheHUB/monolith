import { Helmet } from 'react-helmet';
import { AwardsSection } from './AwardsSection/AwardsSection';
import { FAQSection } from './FAQSection/FAQSection';
import { FooterSection } from './FooterSection/FooterSection';
import { GradingSection } from './GradingSection/GradingSection';
import { JourneySection } from './JourneySection/JourneySection';
import LandingSection from './LandingSection/LandingSection';
import { MentorsAndJudgesSection } from './MentorsAndJudgesSection/MentorsAndJudgesSection';
import { MissionSection } from './MissionSection/MissionSection';
import { NavigationSection } from './NavigationSection/NavigationSection';
import { RecapSection } from './RecapSection/RecapSection';
import { ScheduleSection } from './ScheduleSection/ScheduleSection';
import { SponsorsSection } from './SponsorsSection/SponsorsSection';
import { useFeatureSwitches } from '@/config.ts';

export const HackathonPage = () => {
    const featureSwitches = useFeatureSwitches();
    return (
        <div className="bg-[rgba(255,253,245,1)]">
            <Helmet>
                <title>Hackathon 8.0</title>
                <link rel="icon" href="/faviconHack.ico" />
            </Helmet>

            <NavigationSection />
            <LandingSection />
            <MissionSection />
            <JourneySection />
            <MentorsAndJudgesSection
                mentorsSwitch={featureSwitches.MentorsSwitch}
                jurySwitch={featureSwitches.JurySwitch}
            />
            <ScheduleSection />
            <RecapSection />
            <GradingSection />
            <AwardsSection />
            <FAQSection />
            <SponsorsSection sponsorsSwitch={featureSwitches.SponsorsSwitch} />
            <FooterSection />
        </div>
    );
};
