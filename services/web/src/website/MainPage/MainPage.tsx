import { Fragment } from 'react/jsx-runtime';
import IdentitySection from './AboutSection/components/IdentitySection.tsx';
import PastEventSection from './AboutSection/components/PastEventSection.tsx';
import HackAUBGSection from './HackAUBGSection/HackAUBGSection.tsx';
import { Footer } from './Footer/Footer.tsx';
import MeetTheTeam from './MeetTheTeamSection/components/MeetTheTeam.tsx';
import LandingSection from './LandingSection/LandingSection.tsx';

export const MainPage = () => {
    return (
        <Fragment>
            <LandingSection />
            <div className="about-section rounded-2xl py-8">
                <div className="sm:w-3/5 w-11/12 mx-auto">
                    <IdentitySection />
                    <PastEventSection />
                </div>
            </div>
            <div className="mt-40 bg-[#0a1222] pt-[7.5rem] pb-[7rem]  relative overflow-hidden">
                <MeetTheTeam />
            </div>
            <HackAUBGSection />
            <Footer />
        </Fragment>
    );
};
