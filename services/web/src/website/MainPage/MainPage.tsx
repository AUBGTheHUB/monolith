import { Fragment } from 'react/jsx-runtime';
import IdentitySection from './AboutSection/components/IdentitySection.tsx';
import PastEventSection from './AboutSection/components/PastEventSection.tsx';
import { Footer } from './Footer/Footer.tsx';
import MeetTheTeam from './MeetTheTeamSection/components/MeetTheTeam.tsx';

export const MainPage = () => {
    return (
        <Fragment>
            <div className="about-section rounded-2xl py-8">
                <div className="sm:w-3/5 w-11/12 mx-auto">
                    <IdentitySection />
                    <PastEventSection />
                </div>
            </div>
            <div className="mt-40 bg-[#1E1E1E] py-10 min-h-[58rem] relative overflow-hidden">
                <MeetTheTeam />
            </div>
            <Footer />
        </Fragment>
    );
};
