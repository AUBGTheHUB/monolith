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
            <div className="relative overflow-hidden">
                <div className="about-section bg-white rounded-2xl py-8 z-10 relative">
                    <div className="sm:w-3/5 w-11/12 mx-auto">
                        <IdentitySection />
                        <PastEventSection />
                    </div>
                </div>
                <img
                    src="/meetTheTeam/meet_the_team_blob.svg"
                    className="absolute blur-[10rem] h-[1490.43px] w-[1505.76px] bottom-[0rem] right-[-8rem] opacity-65 rotate-210 z-0"
                ></img>
                <img
                    src="/landingSection/blob-blue.png"
                    alt="a blob"
                    className="absolute opacity-65 blur-[10rem] h-[93rem] right-[0rem] z-0"
                />
                <img
                    src="/landingSection/blob-cyan.png"
                    alt="a blob"
                    className="absolute opacity-65 blur-[10rem] h-[53rem] w-[56rem] right-[-8rem] bottom-[30rem] z-0"
                />
            </div>
            <div className="bg-transparent pt-[7.5rem] pb-[7rem] relative overflow-hidden">
                <MeetTheTeam />
            </div>
            <div className="relative overflow-hidden">
                <HackAUBGSection />
                <img
                    src="/meetTheTeam/meet_the_team_blob.svg"
                    className="absolute blur-[10rem] h-[1490.43px] w-[1505.76px] bottom-[0rem] right-[-8rem] opacity-65 rotate-210 z-0"
                ></img>
                <img
                    src="/footer/footer_blob.svg"
                    className="absolute blur-[12.5rem] h-[852px] top-[-35rem] right-[15rem] opacity-40 rotate-45"
                />
            </div>
            <Footer />
        </Fragment>
    );
};
