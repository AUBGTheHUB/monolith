import React from 'react';
import './main.css';
import { MembersSection } from './MembersSection/MembersSection';
import { NavBar } from './Navigation/NavBar';
import { LandingSection } from './LandingSection/LandingSection';

const LandingHome = () => {
    return (
        <div className="main">
            <NavBar />
            <LandingSection />
            <MembersSection />
        </div>
    );
};

export default LandingHome;
