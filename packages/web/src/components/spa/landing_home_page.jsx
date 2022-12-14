import React from 'react';
import './main.css';
import { Members } from './Members/Members';
import { NavBar } from './Navigation/NavBar';
import { Welcome } from './Welcome_section/Welcome';

const LandingHome = () => {
    return (
        <div className="main">
            <NavBar />
            <Welcome />
            <Members />
        </div>
    );
};

export default LandingHome;
