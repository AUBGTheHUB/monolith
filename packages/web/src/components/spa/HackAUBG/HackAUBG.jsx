import React from 'react';
import { JourneySection } from './JourneySection/JourneySection';
import { MatrixWindow } from './LandingAnimation/LandingAnimation';
import { AboutHackathon } from './AboutHackathon/AboutHackathon';
import { ScheduleHackathon } from './ScheduleSection/ScheduleSection';
import { Anchor, Props } from '../Navigation/NavFactory.js';
import { NavBar } from '../Navigation/NavBar';
import { Footer } from '../Footer/Footer';
import MentorsSection from './MentorsSection/MentorsSection';
import JudgesSection from './JudgesSection/JudgesSection';
import VideoSection from './VideoSection/VideoSection';
import { GradingCriteria } from './GradingCriteria/GradingCriteria';
import { AwardsSection } from '../HackAUBG/AwardsSection/AwardsSection';
import { makeBodyScrollable } from '../Navigation/MobileNav/NavMobile';
import FaqSection from './FaqSection/FaqSection';
import Sponsors from './SponsorsSection/SponsorsSection';
import './hack_aubg.css';

export const HackAUBG = () => {
    makeBodyScrollable();
    document.body.className = 'hackaubg-container';

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
            <JourneySection />
            <MentorsSection />
            <JudgesSection />
            <VideoSection />
            <ScheduleHackathon />
            <GradingCriteria />
            <AwardsSection />
            <Sponsors />
            <FaqSection />
            <Footer
                color={'rgb(25, 183, 0)'}
                iconColor={'rgb(255, 255, 255)'}
                iconBgColor={'rgb(120, 120, 120)'}
            />
        </div>
    );
};
