import React, { useContext } from 'react';
import './main.css';
import { MembersSection } from './MembersSection/MembersSection';
import { NavBar } from './Navigation/NavBar';
import { LandingSection } from './LandingSection/LandingSection';
import { Anchor, Props } from './Navigation/NavFactory.js';
import { Footer } from './Footer/Footer';
import { AboutSection } from './AboutSection/AboutSection';
import '../../../node_modules/react-hovering-cards-carousel/dist/style.css';
import { useEffect } from 'react';
import { checkHashAndScroll } from '../../Global';
import { FsContext } from '../../feature_switches';
import { VerifyAccount } from './HackAUBG/VerifyAccountPop/VerifyAccount.jsx';

const LandingHome = () => {
    document.body.className = 'main-body';

    // eslint-disable-next-line
    const [featureSwitches, _] = useContext(FsContext);

    const anchorList = [
        new Anchor('About', '#about', '', false),
        new Anchor('Team', '#team', '', false, featureSwitches.team),
        new Anchor('Jobs', 'jobs', '', true, featureSwitches.jobs),
    ];

    useEffect(checkHashAndScroll, []);

    return (
        <div className="main">
            <NavBar props={new Props(anchorList, true, 'transparent', false)} />
            <VerifyAccount />
            <LandingSection />
            <AboutSection />
            <MembersSection />
            <Footer
                color={'rgb(21, 76, 121)'}
                iconColor={'rgb(255, 255, 255)'}
                iconBgColor={'rgb(120, 120, 120)'}
                iconSize={'2.2em'}
            />
        </div>
    );
};

export default LandingHome;
