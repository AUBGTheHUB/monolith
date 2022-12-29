import React from 'react';
import './main.css';
import { MembersSection } from './MembersSection/MembersSection';
import { NavBar } from './Navigation/NavBar';
import { LandingSection } from './LandingSection/LandingSection';
import { Anchor, Props } from './Navigation/NavFactory.js';
import { ArticlesSection } from './ArticlesSection/ArticlesSection';
//import { useEffect } from 'react';

const LandingHome = () => {
    const anchorList = [
        new Anchor('About', '#about'),
        new Anchor('Events', '#events'),
        new Anchor('Articles', '#articles'),
        new Anchor('Team', '#team'),
        new Anchor('Jobs', 'jobs')
    ];

    /*eslint-disable no-self-assign*/
    /*
        useEffect(()=> {
        console.log(!!location.hash)
        if(location.hash) 
        setTimeout(()=> location.hash = location.hash,1000)
    },[])*/

    return (
        <div className="main">
            <NavBar props={new Props(anchorList, true)} />
            <LandingSection />
            <ArticlesSection />
            <MembersSection />
        </div>
    );
};

export default LandingHome;
