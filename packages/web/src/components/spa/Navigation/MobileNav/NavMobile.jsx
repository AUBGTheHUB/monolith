import { Button } from './Button';
import React from 'react';
import './mobile_navbar.css';
import { CgMenu } from 'react-icons/cg';
import { MdOutlineClose } from 'react-icons/md';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const makeBodyScrollable = () => {
    document.body.style.position = 'static';
    document.body.style.overflow = 'auto';
};

export const NavMobile = ({ props }) => {
    const [bodyHeight, setBodyHeight] = useState(0);
    let currentBodyHeight = document.documentElement.scrollHeight;

    if (currentBodyHeight !== bodyHeight) {
        setBodyHeight(currentBodyHeight);
    }
    const navigate = useNavigate();

    const renderHackButton = () => {
        if (props.hasHackButton) {
            return (
                <div
                    className="navmobile-button-ham"
                    onClick={navigateToHackAUBG}
                >
                    HackAUBG
                </div>
            );
        }
    };

    const navigateToHackAUBG = () => {
        navigate('/hackaubg');
    };

    const [menuClass, setMenuClass] = useState('navmobile-menu not-displayed');
    const [closeButton, setCloseButton] = useState(
        'navmobile-button-close not-displayed'
    );

    const closeMenu = () => {
        setMenuClass('navmobile-menu-backwards');
    };

    const openHome = () => {
        window.location.href = '/';
    };

    return (
        <div className="navmobile-body">
            <div
                className="navmobile-container"
                style={{
                    backgroundColor: props.mobileBgColor
                        ? props.mobileHeader
                        : 'transparent'
                }}
            >
                <img
                    src="hublogo.png"
                    className="navmobile-logo"
                    onClick={openHome}
                ></img>
                <h2 className="navmobile-title" onClick={openHome}>
                    The Hub
                </h2>
                <Button
                    props={{
                        css: 'navmobile-button',
                        icon: (
                            <CgMenu
                                className="navmobile-button icon"
                                onClick={() => {
                                    setMenuClass('navmobile-menu forwards');
                                    setCloseButton('navmobile-button-close');
                                    document.body.style.position = 'fixed';
                                    document.body.style.overflow = 'scroll';
                                }}
                            />
                        )
                    }}
                />
            </div>

            <div
                className={menuClass}
                style={{
                    height: bodyHeight,
                    backgroundColor: props.mobileBgColor
                }}
            >
                <Button
                    props={{
                        css: 'navmobile-button-close',

                        icon: (
                            <MdOutlineClose
                                className={closeButton}
                                onClick={() => {
                                    setMenuClass('navmobile-menu-backwards');
                                    makeBodyScrollable();
                                }}
                            />
                        )
                    }}
                />

                <div className="navmobile-anchors-container">
                    <ul>
                        {props.anchorList.map((anchor, index) => (
                            <li key={index}>
                                <a
                                    href={anchor.endpoint}
                                    key={index}
                                    onClick={() => {
                                        closeMenu();
                                        makeBodyScrollable();
                                    }}
                                >
                                    {anchor.name}
                                </a>
                            </li>
                        ))}
                    </ul>
                    {renderHackButton()}
                </div>
            </div>
        </div>
    );
};

export { makeBodyScrollable };
