import { Helmet } from 'react-helmet';
import { Navigation } from './NavigationSection/Navigation';
import LandingSection from './LandingSection/LandingSection';
import AboutSection from './AboutSection/AboutSection';
import EventSection from './EventSection/FAQSection';

export default function TournamentPage() {
    return (
        <div>
            <Helmet>
                <title>Gaming Tournament</title>
            </Helmet>
            <Navigation />
            <div className="relative overflow-hidden bg-[color:#061F36] bg-[image:radial-gradient(ellipse_at_20%_40%,#2A506B_0%,#163B59_25%,#061F36_60%)] bg-no-repeat bg-top bg-[length:100%_600px]">
                <div className="hidden xs:block absolute right-0 top-[20dvh] sm:top-[18dvh] lg:top-[calc((80dvh-5rem)/2+3rem)] lg:-translate-y-1/2 h-[34dvh] sm:h-[40dvh] lg:h-[70dvh] translate-x-1/2 opacity-40 sm:opacity-60 lg:opacity-100 pointer-events-none z-0">
                    <img
                        src="/Tournament/hextech.png"
                        alt=""
                        className="h-full w-auto max-w-none object-contain animate-spin [animation-duration:60s]"
                    />
                </div>

                <div className="pointer-events-none absolute inset-x-0 bottom-0 h-[500px] z-0 bg-[image:radial-gradient(ellipse_at_90%_100%,rgba(199,155,59,0.35)_0%,transparent_60%)]" />

                <div className="relative z-10">
                    <LandingSection />
                    <AboutSection />
                    <EventSection />
                </div>
            </div>
        </div>
    );
}
