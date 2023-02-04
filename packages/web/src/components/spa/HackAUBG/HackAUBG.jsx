import React from 'react';
import './hackAUBG.css';
import { JourneySection } from './JourneySection/JourneySection';

import { MatrixWindow } from './LandingAnimation/LandingAnimation';
import { Anchor, Props } from '../Navigation/NavFactory.js';
import { NavBar } from '../Navigation/NavBar';

export const HackAUBG = () => {
    const anchorList = [
        new Anchor('About', '#about'),
        new Anchor('Schedule', '#schedule'),
        new Anchor('Grading Criteria', '#grading'),
        new Anchor('FAQ', '#faq')
    ];

    return (
        <div className="hackaubg-container">
            <NavBar props={new Props(anchorList, false, 'rgba(0,0,0,.5)')} />
            <MatrixWindow />
            <JourneySection />
        </div>
    );
};
