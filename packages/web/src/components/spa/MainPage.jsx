import React from 'react';
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

const LandingHome = () => {
    const anchorList = [
        new Anchor('About', '#AboutSection'),
        new Anchor('Team', '#team'),
        new Anchor('Jobs', 'jobs')
    ];

    useEffect(checkHashAndScroll, []);

    return (
        <div className="main">
            <NavBar props={new Props(anchorList, true, 'transparent', false)} />
            <LandingSection />
            <AboutSection />
            <MembersSection />
            <Footer
                color={'rgb(21, 76, 121)'}
                iconColor={'rgb(255, 255, 255)'}
                iconBgColor={'rgb(120, 120, 120)'}
            />
        </div>
    );
};

export default LandingHome;
