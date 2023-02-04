import React from 'react';
import './hackAUBG.css';

import { MatrixWindow } from './LandingAnimation/LandingAnimation';
import { AboutHackathon } from './AboutHackathon/AboutHackathon';
import { Anchor, Props } from '../Navigation/NavFactory.js';
import { NavBar } from '../Navigation/NavBar';
import { Footer } from '../Footer/Footer';
import MentorsSection from './MentorsSection/MentorsSection';
import JudgesSection from './JudgesSection/JudgesSection';
import VideoSection from './VideoSection/VideoSection';
import FaqSection from './FaqSection/FaqSection';

export const HackAUBG = () => {
    const anchorList = [
        new Anchor('About', '#AboutSection'),
        new Anchor('Schedule', '#team'),
        new Anchor('Grading criteria', 'jobs'),
        new Anchor('FAQ', 'jobs')
    ];

    return (
        <div className="hackaubg-container">
            <NavBar props={new Props(anchorList, false, 'rgba(0,0,0,.5)')} />
            <MatrixWindow />
            <AboutHackathon />
            <VideoSection />
            <MentorsSection />
            <JudgesSection />
            <FaqSection />
            <Footer colour={'rgb(25, 183, 0)'} />
        </div>
    );
};
