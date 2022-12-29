import React from 'react';
import './page_not_found.css';
import { NavBar } from '../spa/Navigation/NavBar';
import { Anchor, Props } from '../spa/Navigation/NavFactory';

const anchorList = [
    new Anchor('About', '/#about'),
    new Anchor('Events', '/#events'),
    new Anchor('Articles', '/#articles'),
    new Anchor('Team', '/#team'),
    new Anchor('Jobs', '/jobs')
];

const NotFound = () => {
    return (
        <div className="background">
            <NavBar props={new Props(anchorList, true)} />
            <div className="hubzie-404-image">
                <img
                    src="hubzzie.png"
                    className="hubzie-404-image"
                    alt="Hubzie-404-not-found"
                />
            </div>
        </div>
    );
};

export default NotFound;
