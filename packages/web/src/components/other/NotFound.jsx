import React from 'react';
import './page_not_found.css';
//import './desktop_navbar.css';
//import { NavBar } from '../spa/Navigation/NavBar';
// import { Anchor, Props } from '../spa/Navigation/NavFactory';

// const anchorList = [
//     new Anchor('About', '/#about'),
//     new Anchor('Events', '/#events'),
//     new Anchor('Articles', '/#articles'),
//     new Anchor('Team', '/#team'),
//     new Anchor('Jobs', '/jobs')
// ];

const NotFound = () => {
    return (
        <div className="background-not-found">
            {   <div className="navdesktop-container">
                    <div className="navdesktop-logo">
                        <img
                            src="/hublogo.png"
                            className="navdesktop-logo-image"
                            alt="The Hub AUBG"
                        />
                        <p>The Hub</p>
                    </div>
                </div>
            }
            <div className="container-text-404">
                <div>
                    <h1 className="heading-text-404">404</h1>
                    <h2 className="mid-heading-404">Page not found</h2>
                    <p className="paragraph-404">
                        Seems like the page you are looking for got abducted by
                        aliens...
                    </p>
                    <button
                        className="button-404"
                        type="button"
                        onClick={() => {
                            location.href = '/';
                        }}
                    >
                        Back to Homepage
                    </button>
                </div>
                <div className="hubzie-UFO-image">
                    <img
                        src="/hubzieUFOimage.png"
                        className="hubzie-UFO-image"
                        alt="Hubzie being abducted by a UFO"
                    />
                </div>
            </div>
        </div>
    );
};

export default NotFound;
