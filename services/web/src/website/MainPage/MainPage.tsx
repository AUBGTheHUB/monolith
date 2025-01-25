import IdentitySection from './AboutSection/components/IdentitySection.tsx';
import PastEventSection from './AboutSection/components/PastEventSection.tsx';
import { Navigation } from './Navigation/Navigation.tsx';

import './stylesheet.css';

export const MainPage = () => {
    return (
        <div className="main-page">
            <Navigation />
            <div className="about-section rounded-2xl py-8">
                <div className="sm:w-3/5 w-11/12 mx-auto">
                    <IdentitySection />
                    <PastEventSection />
                </div>
            </div>
        </div>
    );
};
