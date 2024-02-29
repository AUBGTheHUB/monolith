import React from 'react';
import { JourneySection } from './JourneySection/JourneySection';
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
import { FAQSection } from './FAQSection/FAQSection.jsx';
import Sponsors from './SponsorsSection/SponsorsSection';
import './hack_aubg.css';
import { LandingPage } from './LandingPage/LandingPage.jsx';
import { FaRegLightbulb } from 'react-icons/fa';
import { useLocation } from 'react-router-dom';
import { VerifyAccount } from '../HackAUBG/VerifyAccountPop/VerifyAccount.jsx';
import { useState, useEffect } from 'react';
import { Outlet } from 'react-router-dom';

export const HackAUBG = () => {
    const [showVerification, setShowVerification] = useState('');

    document.body.className = 'hackaubg-container';

    const anchorList = [
        new Anchor('About', '#about'),
        new Anchor('Schedule', '#schedule'),
        new Anchor('Grading Criteria', '#grading'),
        new Anchor('FAQ', '#faq', <FaRegLightbulb />),
    ];

    const location = useLocation();
    if (location.search.includes('/verify')) {
        console.log('verify');
    }
    const params = new URLSearchParams(location.search);
    const jwtToken = params.get('jwt_token');
    useEffect(() => {
        if (location.pathname === '/hackaubg/verify') {
            console.log('verify');
            setShowVerification(jwtToken);
        }
    }, [location]);

    useEffect(() => {
        document.body.style.overflow = showVerification ? 'hidden' : 'auto';
    }, [showVerification]);

    const handleVerificationSuccess = () => {
        setShowVerification(false);
    };

    return (
        <div className={`hackaubg-container ${showVerification ? 'showVerification' : ''}`}>
            <div className={showVerification ? 'blur' : ''}>
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
                            'hackAUBG', // specify HackAUBG page
                        )
                    }
                />
                <LandingPage />
                <AboutHackathon />
                <JourneySection />
                <RegistrationForm />
                <MentorsSection />
                <JudgesSection />
                <VideoSection />
                <ScheduleHackathon />
                <GradingCriteria />
                <AwardsSection />
                <Sponsors />
                <FAQSection />
                <Footer
                    color={'rgba(220,193,255,255)'}
                    iconColor={'rgb(0, 0, 0)'}
                    iconBgColor={'rgba(0, 0, 0, 0)'}
                    textColor={'#000'}
                    iconSize={'2.6em'}
                />
            </div>
            {showVerification && <VerifyAccount className="no-blur" onSuccess={handleVerificationSuccess} />}
            <Outlet />
        </div>
    );
};
