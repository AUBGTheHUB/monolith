import { Fragment } from 'react/jsx-runtime';
import IdentitySection from './AboutSection/components/IdentitySection.tsx';
import PastEventSection from './AboutSection/components/PastEventSection.tsx';
import HackAUBGSection from './HackAUBGSection/HackAUBGSection.tsx';
import { Footer } from './Footer/Footer.tsx';
import MeetTheTeam from './MeetTheTeamSection/components/MeetTheTeam.tsx';
import LandingSection from './LandingSection/LandingSection.tsx';
import { useFeatureSwitches } from '@/config.ts';

export const MainPage = () => {
    const featureSwitches = useFeatureSwitches();

    return (
        <Fragment>
            <LandingSection />
            <div className="relative overflow-hidden">
                <div className="about-section bg-white rounded-2xl py-8 z-10 relative">
                    <div className="sm:w-3/5 w-11/12 mx-auto">
                        <IdentitySection />
                        <PastEventSection />
                    </div>
                </div>
                <img
                    src="/landingSection/gradient-top.png"
                    alt="a gradient"
                    className="absolute pointer-events-none h-[93rem] right-[0rem] z-0"
                />
                <img
                    src="/meetTheTeam/gradient-meet-the-team.png"
                    className="absolute pointer-events-none h-[1490.43px] w-[1505.76px] bottom-[0rem] right-[-8rem] rotate-210 z-0"
                />
                <img
                    src="/footer/footer-gradient.png"
                    alt="a gradient"
                    className="absolute pointer-events-none h-[53rem] w-[56rem] right-[-8rem] top-[-30rem] z-0"
                />
            </div>
            <div className="bg-transparent pt-[7.5rem] pb-[7rem] relative overflow-hidden" id="meet-team">
                <MeetTheTeam />
            </div>
            <div className="relative overflow-hidden">
                <HackAUBGSection mentorsSwitch={featureSwitches.MentorsSwitch} />
                <img
                    src="/meetTheTeam/gradient-meet-the-team.png"
                    className="absolute pointer-events-none h-[1490.43px] w-[1505.76px] bottom-[0rem] right-[-8rem] rotate-210 z-0"
                ></img>
                <img
                    src="/footer/footer-gradient.png"
                    className="absolute pointer-events-none h-[852px] top-[-35rem] right-[15rem] rotate-45"
                />
            </div>
            <Footer />
        </Fragment>
    );
};
