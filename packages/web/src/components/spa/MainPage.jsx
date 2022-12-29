import React from 'react';
import './main.css';
import { MembersSection } from './MembersSection/MembersSection';
import { NavBar } from './Navigation/NavBar';
import { LandingSection } from './LandingSection/LandingSection';
import { Anchor, Props } from './Navigation/NavFactory.js';
import { ArticlesSection } from './ArticlesSection/ArticlesSection';
import { useEffect } from 'react';
// import $ from 'jquery';

const LandingHome = () => {
    const anchorList = [
        new Anchor('About', '#about'),
        new Anchor('Events', '#events'),
        new Anchor('Articles', '#articles'),
        new Anchor('Team', '#team'),
        new Anchor('Jobs', 'jobs')
    ];

    useEffect(() => {
        let hasHash = !!location.hash;
        if (hasHash) {
            /*
                check if document.getElementById is null
                -> if null -> skip
                -> if not null -> trigger .scrollIntoView()

                ---

                try to fix not scrolling into full view
            */

            setTimeout(() => {
                document
                    .getElementById(location.hash.replace('#', ''))
                    .scrollIntoView();
            }, 600);
        }
    }, []);

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
