import React from 'react';
import './hackAUBG.css';

import { MatrixWindow } from './LandingAnimation/LandingAnimation';
import { Anchor, Props } from './Navigation/NavFactory.js';
import { NavBar } from './Navigation/NavBar';

export const HackAUBG = () => {
    const anchorList = [
        new Anchor('About', '#AboutSection'),
        // new Anchor('Events', '#events'),
        // new Anchor('Articles', '#articles'),
        new Anchor('Team', '#team'),
        new Anchor('Jobs', 'jobs')
    ];

    return (
        <div className="hackaubg-container">
            <NavBar props={new Props(anchorList, true)} />
            <MatrixWindow />
        </div>
    );
};
