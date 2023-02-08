import React from 'react';
import { MatrixWindow } from './LandingAnimation/LandingAnimation';
import { AboutHackathon } from './AboutHackathon/AboutHackathon';
import { ScheduleHackathon } from './ScheduleSection/ScheduleSection';
import { Anchor, Props } from '../Navigation/NavFactory.js';
import { NavBar } from '../Navigation/NavBar';
import { Footer } from '../Footer/Footer';
import { GradingCriteria } from './GradingCriteria/GradingCriteria';
import { makeBodyScrollable } from '../Navigation/MobileNav/NavMobile';
import { TopButton } from './TopButton/TopButton';

export const HackAUBG = () => {
    makeBodyScrollable();

    const anchorList = [
        new Anchor('About', '#AboutSection'),
        // new Anchor('Events', '#events'),
        // new Anchor('Articles', '#articles'),
        new Anchor('Schedule', '#team'),
        new Anchor('Grading criteria', 'jobs'),
        new Anchor('FAQ', 'jobs')
    ];

    return (
        <div className="hackaubg-container">
            <NavBar
                props={
                    new Props(
                        anchorList,
                        false,
                        'rgba(0,0,0,.5)',
                        true,
                        '#222222',
                        'red'
                    )
                }
            />
            <TopButton />
            <MatrixWindow />
            <AboutHackathon />
            <ScheduleHackathon />
            <GradingCriteria />
            <Footer colour={'rgb(25, 183, 0)'} />
        </div>
    );
};
