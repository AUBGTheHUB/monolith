import React from 'react';
import './main.css';
import { MembersSection } from './MembersSection/MembersSection';
import { NavBar } from './Navigation/NavBar';
import { LandingSection } from './LandingSection/LandingSection';
import { Anchor, Props } from './Navigation/NavFactory.js';
import { ArticlesSection } from './ArticlesSection/ArticlesSection';
import { useEffect } from 'react';
import { Footer } from './Footer/Footer';
import { AboutSection } from './AboutSection/AboutSection';

const LandingHome = () => {
    const anchorList = [
        new Anchor('About', '#AboutSection'),
        // new Anchor('Events', '#events'),
        // new Anchor('Articles', '#articles'),
        new Anchor('Team', '#team'),
        new Anchor('Jobs', 'jobs')
    ];

    useEffect(() => {
        let hasHash = !!location.hash;
        if (hasHash) {
            /*if (document.getElementById != null)
            {
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
            //}
        }
    }, []);

    return (
        <div className="main">
            {/* spacing of buttons should be fixed -- page overflow is disabled in main.css */}
            <NavBar props={new Props(anchorList, true, 'transparent')} />
            <LandingSection />
            <AboutSection />
            <ArticlesSection />
            <MembersSection />
            <Footer />
        </div>
    );
};

export default LandingHome;
