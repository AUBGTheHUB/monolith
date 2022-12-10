import React from 'react';
import './main.css';
import { NavBar } from './Navigation/NavBar';
import { Welcome } from './Welcome_section/Welcome';

const LandingHome = () => {
    return (
        <div className="main">
            <NavBar />
            <Welcome />
        </div>
    );
};

export default LandingHome;
