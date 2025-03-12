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
                    <div className="sm:w-3/5 w-11/12 mx-auto z-10">
                        <IdentitySection />
                        <PastEventSection />
                    </div>
                </div>
                <img
                    src="https://hubarskibucket.s3.eu-central-1.amazonaws.com/the-hub-2025/website-elements/gradient-top.webp"
                    alt="a gradient"
                    className="absolute pointer-events-none hidden sm:block h-[80rem] w-full top-[-30rem] right-[0rem] z-0"
                />
                <img
                    src="https://hubarskibucket.s3.eu-central-1.amazonaws.com/the-hub-2025/website-elements/gradient-meet-the-team.webp"
                    className="absolute pointer-events-none hidden sm:block h-[80rem] w-full bottom-[40rem] right-[0rem] rotate-210 z-0"
                ></img>
            </div>
            <div className="bg-transparent pt-[7.5rem] pb-[7rem] relative overflow-hidden" id="meet-team">
                <MeetTheTeam />
            </div>
            <div className="relative overflow-hidden">
                <HackAUBGSection mentorsSwitch={featureSwitches.MentorsSwitch} />
                <img
                    src="https://hubarskibucket.s3.eu-central-1.amazonaws.com/the-hub-2025/website-elements/gradient-meet-the-team.webp"
                    className="absolute pointer-events-none h-[1490.43px] w-[1505.76px] bottom-[0rem] right-[-8rem] rotate-210 z-0"
                ></img>
                <img
                    src="https://hubarskibucket.s3.eu-central-1.amazonaws.com/the-hub-2025/website-elements/footer-gradient.webp"
                    className="absolute h-[70rem] bottom-[-19rem] sm:bottom-[-15rem] right-[-14rem] sm:right-[-23rem] pointer-events-none w-screen"
                />
            </div>
            <Footer />
        </Fragment>
    );
};
