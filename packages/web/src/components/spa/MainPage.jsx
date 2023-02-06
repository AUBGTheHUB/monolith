import React from 'react';
import './main.css';
import { MembersSection } from './MembersSection/MembersSection';
import { NavBar } from './Navigation/NavBar';
import { LandingSection } from './LandingSection/LandingSection';
import { Footer } from './Footer/Footer';
import { AboutSection } from './AboutSection/AboutSection';
import { Anchor, Props } from './Navigation/NavFactory.js';
import '../../../node_modules/react-hovering-cards-carousel/dist/style.css';
import { useEffect } from 'react';

const LandingHome = () => {
    const anchorList = [
        new Anchor('About', '#AboutSection'),
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
            <NavBar props={new Props(anchorList, true, 'transparent', false)} />
            <LandingSection />
            <AboutSection />
            <MembersSection />
            <Footer colour={'rgb(21, 76, 121)'} />
        </div>
    );
};

export default LandingHome;
