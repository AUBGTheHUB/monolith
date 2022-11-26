import { Button } from './Button';
import React from 'react';
import './style.css';
import { GiHamburgerMenu } from 'react-icons/gi';
import { AiOutlineClose } from 'react-icons/ai';
import { useState } from 'react';

export const NavMobile = () => {
    const [menuClass, setMenuClass] = useState('navmobile-menu not-displayed');
    const [closeButton, setCloseButton] = useState(
        'navmobile-button-close not-displayed'
    );
    return (
        <>
            <div className="navmobile-container">
                <Button
                    props={{
                        css: 'navmobile-button',
                        icon: (
                            <GiHamburgerMenu
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
                            <AiOutlineClose
                                className={closeButton}
                                onClick={() => {
                                    console.log('XXX');
                                    // setCloseButton(
                                    //     'navmobile-button-close not-displayed'
                                    // );
                                    setMenuClass('navmobile-menu backwards');
                                    console.log(menuClass);
                                }}
                            />
                        )
                    }}
                />
            </div>
        </>
    );
};
