import React from 'react';
import { MatrixWindow } from './LandingAnimation/LandingAnimation';
import { AboutHackathon } from './AboutHackathon/AboutHackathon';
import { ScheduleHackathon } from './ScheduleSection/ScheduleSection';
import { Anchor, Props } from '../Navigation/NavFactory.js';
import { NavBar } from '../Navigation/NavBar';
import { Footer } from '../Footer/Footer';
import VideoSection from './VideoSection/VideoSection';
import { GradingCriteria } from './GradingCriteria/GradingCriteria';
import { makeBodyScrollable } from '../Navigation/MobileNav/NavMobile';
import FaqSection from './FaqSection/FaqSection';

export const HackAUBG = () => {
    makeBodyScrollable();

    const anchorList = [
        new Anchor('About', '#AboutSection'),
        new Anchor('Schedule', '#team'),
        new Anchor('Grading criteria', 'jobs'),
        new Anchor('FAQ', 'jobs')
    ];

    return (
        <div className="hackaubg-container">
            <NavBar
                props={
                    new Props(
                        anchorList, // list of anchors
                        false, // hackAUBG button
                        'rgba(0,0,0,.5)', // desktop background color nav
                        true, // sticky desktop nav
                        '#222222', // mobile nav background color when not opened (default transparent)
                        'gray', // mobile background color nav when opened
                        'white', // anchor color
                        'green', // desktop anchor hover color
                        'dark gray' // mobile anchor hover color
                    )
                }
            />
            <MatrixWindow />
            <AboutHackathon />
            <VideoSection />
            <ScheduleHackathon />
            <GradingCriteria />
            <FaqSection />
            <Footer colour={'rgb(25, 183, 0)'} />
        </div>
    );
};
