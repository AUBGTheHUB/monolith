import React from 'react';
import './footer.css';
import { FaFacebookSquare } from 'react-icons/fa';
import { GrInstagram } from 'react-icons/gr';
import { AiFillYoutube } from 'react-icons/ai';
import { openNewTab } from '../../../Global';

export const Footer = ({ color, iconColor, iconBgColor }) => {
    return (
        <div className="footer-container" style={{ backgroundColor: color }}>
            <div className="copyright">
                <p>© 2023 The Hub AUBG. All rights reserved</p>
            </div>
            <div className="social-media">
                <div className="links" style={{ backgroundColor: iconBgColor }}>
                    <div
                        className="footer-icon"
                        onClick={() => {
                            openNewTab('https://facebook.com/TheHubAUBG');
                        }}
                    >
                        <FaFacebookSquare style={{ color: iconColor }} />
                    </div>
                </div>
                <div className="links" style={{ backgroundColor: iconBgColor }}>
                    <div
                        className="footer-icon"
                        onClick={() => {
                            openNewTab('https://instagram.com/thehubaubg/');
                        }}
                    >
                        <GrInstagram style={{ color: iconColor }} />
                    </div>
                </div>
                <div className="links" style={{ backgroundColor: iconBgColor }}>
                    <div
                        className="footer-icon"
                        onClick={() => {
                            openNewTab(
                                'https://youtube.com/channel/UChdtBZBvaK9XZurP3GjPDug'
                            );
                        }}
                    >
                        <AiFillYoutube style={{ color: iconColor }} />
                    </div>
                </div>
            </div>
        </div>
    );
};
