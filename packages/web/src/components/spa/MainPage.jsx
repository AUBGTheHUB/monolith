import React from 'react';
import './main.css';
import { MembersSection } from './MembersSection/MembersSection';
import { NavBar } from './Navigation/NavBar';
import { LandingSection } from './LandingSection/LandingSection';
import { Anchor, Props } from './Navigation/NavFactory.js';

const LandingHome = () => {
    const anchorList = [
        new Anchor('About', '#about'),
        new Anchor('Events', '#events'),
        new Anchor('Articles', '#articles'),
        new Anchor('Team', '#team'),
        new Anchor('Jobs', 'jobs')
    ];

    return (
        <div className="main">
            <NavBar props={new Props(anchorList, true)} />
            <LandingSection />
            <MembersSection />
        </div>
    );
};

export default LandingHome;
