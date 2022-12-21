import React from 'react';
import './desktop_navbar.css';

export const NavDesktop = ({ props }) => {
    const renderHackButton = () => {
        if (props.hasHackButton) {
            return (
                <button
                    className="hackaubg-btn"
                    type="button"
                    onClick={() => {
                        location.href = '/hackaubg';
                    }}
                >
                    <p>HackAUBG</p>
                </button>
            );
        }
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
                        <a
                            href={anchor.endpoint}
                            key={index}
                            className="navdesktop-navtags"
                        >
                            {anchor.name}
                        </a>
                    </div>
                ))}
                {renderHackButton()}
            </div>
        </div>
    );
};
