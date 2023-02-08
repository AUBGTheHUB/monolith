import React from 'react';
import './footer.css';
import { FaFacebookSquare } from 'react-icons/fa';
import { GrInstagram } from 'react-icons/gr';
import { AiFillYoutube } from 'react-icons/ai';

export const Footer = ({ colour }) => {
    return (
        <div className="footer-container" style={{ backgroundColor: colour }}>
            <div className="copyright">
                <p>© 2023 The Hub AUBG. All rights reserved</p>
            </div>
            <div className="social-media">
                <div className="links">
                    <a href="https://www.facebook.com/TheHubAUBG">
                        <FaFacebookSquare />
                    </a>
                </div>
                <div className="links">
                    <a href="https://www.instagram.com/thehubaubg/">
                        <GrInstagram />
                    </a>
                </div>
                <div className="links">
                    <a href="https://www.youtube.com/channel/UChdtBZBvaK9XZurP3GjPDug">
                        <AiFillYoutube />
                    </a>
                </div>
            </div>
        </div>
    );
};
