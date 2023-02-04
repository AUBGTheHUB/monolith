import React from 'react';
import './desktop_navbar.css';

export const NavDesktop = ({ props }) => {
    const renderHackButton = () => {
       
    };
    return (
        <div className="navdesktop-container">
            <div className="navdesktop-logo">
                <img
                    src="hublogo.png"
                    className="navdesktop-logo-image"
                    alt="The Hub AUBG"
                />
                <p>The Hub</p>
            </div>
            <div className="navdesktop-buttons">
                {props.anchorList.map((anchor, index) => (
                    <div className="navdesktop-navdivs" key={index}>
                        <a href={anchor.endpoint} key={index}>
                            {anchor.name}
                        </a>
                    </div>
                ))}
                {renderHackButton()}
            </div>
        </div>
    );
};
