import { Button } from './Button';
import React from 'react';
import './style.css';
// import { GiHamburgerMenu } from 'react-icons/gi';
// import { IoIosClose } from 'react-icons/io';
import { CgMenu } from 'react-icons/cg';
import { MdOutlineClose } from 'react-icons/md';

import { useState } from 'react';
export const NavMobile = () => {
    const [menuClass, setMenuClass] = useState('navmobile-menu not-displayed');
    const [closeButton, setCloseButton] = useState(
        'navmobile-button-close not-displayed'
    );

    const closeMenu = () => {
        setMenuClass('navmobile-menu-backwards');
    };

    return (
        <div className="navmobile-body">
            <div className="navmobile-logo">
                <img src="hublogo.png"></img>
            </div>
            <div className="navmobile-title">
                <h2>The Hub</h2>
            </div>
            <div className="navmobile-container">
                <Button
                    props={{
                        css: 'navmobile-button',
                        icon: (
                            <CgMenu
                                className="navmobile-button icon"
                                onClick={() => {
                                    setMenuClass('navmobile-menu forwards');
                                    setCloseButton('navmobile-button-close');
                                }}
                            />
                        )
                    }}
                />
            </div>

            <div className={menuClass}>
                <Button
                    props={{
                        css: 'navmobile-button',
                        icon: (
                            <MdOutlineClose
                                className={closeButton}
                                onClick={() => {
                                    setMenuClass('navmobile-menu-backwards');
                                }}
                            />
                        )
                    }}
                />

                {/* Anchors are clickable / selectable */}

                <div className="navmobile-anchors-container">
                    <ul>
                        <li>
                            <a href="#about" onClick={closeMenu}>
                                About
                            </a>
                        </li>
                        <li>
                            <a href="#events" onClick={closeMenu}>
                                Events
                            </a>
                        </li>
                        <li>
                            <a href="#articles" onClick={closeMenu}>
                                Articles
                            </a>
                        </li>
                        <li>
                            <a href="#team" onClick={closeMenu}>
                                Team
                            </a>
                        </li>
                        <li>
                            <a href="#jobs" onClick={closeMenu}>
                                Jobs
                            </a>
                        </li>
                        <li>
                            <a href="#hackaubg" onClick={closeMenu}>
                                HackAUBG
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    );
};
