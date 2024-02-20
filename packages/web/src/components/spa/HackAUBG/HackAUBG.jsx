import React from 'react';
import { JourneySection } from './JourneySection/JourneySection';
// import { MatrixWindow } from './LandingAnimation/LandingAnimation';
import { AboutHackathon } from './AboutHackathon/AboutHackathon';
import { ScheduleHackathon } from './ScheduleSection/ScheduleSection';
import { Anchor, Props } from '../Navigation/NavFactory.js';
import { NavBar } from '../Navigation/NavBar';
import { Footer } from '../Footer/Footer';
import MentorsSection from './MentorsSection/MentorsSection';
import JudgesSection from './JudgesSection/JudgesSection';
import VideoSection from './VideoSection/VideoSection';
import RegistrationForm from './RegistrationForm/RegistrationForm.jsx';
import { GradingCriteria } from './GradingCriteria/GradingCriteria';
import { AwardsSection } from '../HackAUBG/AwardsSection/AwardsSection';
import { makeBodyScrollable } from '../Navigation/MobileNav/NavMobile';
import FaqSection from './FaqSection/FaqSection';
import Sponsors from './SponsorsSection/SponsorsSection';
import './hack_aubg.css';
import { LandingPage } from './LandingPage/LandingPage.jsx';
import { FaRegLightbulb } from 'react-icons/fa';

export const HackAUBG = () => {
    makeBodyScrollable();

    document.body.className = 'hackaubg-container';

    const anchorList = [
        new Anchor('About', '#about'),
        new Anchor('Schedule', '#schedule'),
        new Anchor('Grading Criteria', '#grading'),
        new Anchor('FAQ', '#faq', <FaRegLightbulb />),
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
                        '#e2d7fc', // anchor color
                        'hackAUBG', // specify HackAUBG
                    )
                }
            />
            <LandingPage />

            <AboutHackathon />
            <JourneySection />
            <MentorsSection />
            <JudgesSection />
            <RegistrationForm />
            <VideoSection />
            <ScheduleHackathon />
            <GradingCriteria />
            <AwardsSection />
            <Sponsors />
            <FaqSection />
            <Footer
                color={'rgba(220,193,255,255)'}
                iconColor={'rgb(0, 0, 0)'}
                iconBgColor={'rgba(0, 0, 0, 0)'}
                textColor={'#000'}
                iconSize={'2.6em'}
            />
        </div>
    );
};
