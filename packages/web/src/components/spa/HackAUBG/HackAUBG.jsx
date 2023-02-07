import React from 'react';
import { JourneySection } from './JourneySection/JourneySection';
import { MatrixWindow } from './LandingAnimation/LandingAnimation';
import { AboutHackathon } from './AboutHackathon/AboutHackathon';
import { ScheduleHackathon } from './ScheduleSection/ScheduleSection';
import { Anchor, Props } from '../Navigation/NavFactory.js';
import { NavBar } from '../Navigation/NavBar';
import { Footer } from '../Footer/Footer';
import { GradingCriteria } from './GradingCriteria/GradingCriteria';
import { makeBodyScrollable } from '../Navigation/MobileNav/NavMobile';

export const HackAUBG = () => {
    makeBodyScrollable();

    const anchorList = [
        new Anchor('About', '#about'),
        new Anchor('Schedule', '#schedule'),
        new Anchor('Grading Criteria', '#grading'),
        new Anchor('FAQ', '#faq')
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
            <MatrixWindow />
            <AboutHackathon />
            <JourneySection />
            <ScheduleHackathon />
            <GradingCriteria />
            <Footer colour={'rgb(25, 183, 0)'} />
        </div>
    );
};
