import React from 'react';
import './desktop_navbar.css';
import { navigateTo } from '../../../../Global';
import { Link } from 'react-router-dom';

export const NavDesktop = ({ props }) => {
    const renderHackButton = () => {
        if (props.hasHackButton) {
            return (
                <button
                    className="hackaubg-btn"
                    type="button"
                    onClick={() => {
                        navigateTo('/hackaubg');
                    }}>
                    <p>HackAUBG</p>
                </button>
            );
        }
    };

    const openHome = () => {
        navigateTo('/');
        window.scrollTo(0, 0);
    };

    const stickyProps = () => {
        if (props.isSticky) {
            return {
                backgroundColor: props.bgColor,
                position: 'fixed',
                top: 0,
                width: '100vw',
                zIndex: 1,
            };
        }

        return {
            backgroundColor: props.bgColor,
        };
    };

    const changeAnchorColor = (e, color) => {
        e.target.style.color = color;
    };

    const buildDesktopAnchor = anchor => {
        if (anchor.isLink) {
            return (
                <Link
                    to={anchor.endpoint}
                    onMouseEnter={e => {
                        changeAnchorColor(e, props.anchorHoverColor);
                    }}
                    onMouseLeave={e => {
                        changeAnchorColor(e, props.anchorColor);
                    }}
                    style={{ color: props.anchorColor }}>
                    {anchor.name}
                </Link>
            );
        }

        return (
            <a
                href={anchor.endpoint}
                onMouseEnter={e => {
                    changeAnchorColor(e, props.anchorHoverColor);
                }}
                onMouseLeave={e => {
                    changeAnchorColor(e, props.anchorColor);
                }}
                style={{ color: props.anchorColor }}>
                {anchor.name}
                <div className="anchor-icon">{anchor.image}</div>
            </a>
        );
    };

    return (
        <div className="navdesktop-container" style={stickyProps()}>
            <div className="navdesktop-logo" onClick={openHome}>
                <img src="hublogo.png" className="navdesktop-logo-image" alt="The Hub AUBG" />
                <p>The Hub</p>
            </div>
            <div className="navdesktop-flex-buttons">
                <div className="navdesktop-buttons">
                    {props.anchorList.map((anchor, index) => (
                        <div
                            className="navdesktop-navdivs"
                            key={index}
                            style={{
                                display: !anchor.featureSwitch ? 'none' : '',
                            }}>
                            {buildDesktopAnchor(anchor)}
                        </div>
                    ))}
                </div>
                {renderHackButton()}
            </div>
        </div>
    );
};
