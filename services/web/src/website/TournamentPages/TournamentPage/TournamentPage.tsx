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
                <div className="pointer-events-none absolute right-0 top-[min(14vw,200px)] z-0 hidden h-[min(47vw,680px)] translate-x-[52%] sm:block xl:top-[6vw] 2xl:-top-4">
                    <img
                        src="/Tournament/hextech.png"
                        alt=""
                        className="h-full w-auto max-w-none animate-[spin_60s_linear_infinite] object-contain"
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
