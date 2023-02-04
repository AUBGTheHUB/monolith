import React from 'react';
import './hackAUBG.css';
import { MatrixWindow } from './LandingAnimation/LandingAnimation';
import { AboutHackathon } from './AboutHackathon/AboutHackathon';

export const HackAUBG = () => {
    return (
        <div className="hackaubg-container">
            <MatrixWindow />
            <AboutHackathon />
        </div>
    );
};
