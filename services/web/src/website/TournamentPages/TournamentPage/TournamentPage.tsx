import { Helmet } from 'react-helmet';
import { Navigation } from './NavigationSection/Navigation';
import LandingSection from './LandingSection/LandingSection';
import AboutSection from './AboutSection/AboutSection';
import EventSection from './EventSection/FAQSection';

export default function TournamentPage() {
    return (
        <div className="bg-[#061F36]">
            <Helmet>
                <title>Gaming Tournament</title>
            </Helmet>
            <img
                src="/Tournament/hextech.png"
                alt="Right background hextech image"
                className="right-0 top-[150px] md:top-[210px] invisible xs:visible absolute h-[35%] sm:h-[40%] lg:h-[60%] w-auto object-cover pointer-events-none"
            />
            <Navigation />
            <LandingSection />
            <AboutSection />
            <EventSection />
        </div>
    );
}
