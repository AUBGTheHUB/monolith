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

    const openHome = () => {
        window.location.href = '/';
    };

    const stickyProps = () => {
        if (props.isSticky) {
            return {
                backgroundColor: props.bgColor,
                position: 'fixed',
                top: 0,
                width: '100vw'
            };
        }

        return {
            backgroundColor: props.bgColor
        };
    };

    const changeAnchorColor = (e, color) => {
        e.target.style.color = color;
    };

    return (
        <div className="navdesktop-container" style={stickyProps()}>
            <div className="navdesktop-logo" onClick={openHome}>
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
                            onMouseEnter={(e) => {
                                changeAnchorColor(e, props.anchorHoverColor);
                            }}
                            onMouseLeave={(e) => {
                                changeAnchorColor(e, props.anchorColor);
                            }}
                            style={{ color: props.anchorColor }}
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
