import React from 'react';
import './footer.css';
import { FaFacebookSquare } from 'react-icons/fa';
import { GrInstagram } from 'react-icons/gr';
import { AiFillYoutube } from 'react-icons/ai';

export const Footer = ({ colour, iconcolor }) => {
    return (
        <div className="footer-container" style={{ backgroundColor: colour }}>
            <div className="copyright">
                <p>© 2023 The Hub AUBG. All rights reserved</p>
            </div>
            <div className="social-media">
                <div className="links">
                    <a
                        href="https://www.facebook.com/TheHubAUBG"
                        target="_blank"
                    >
                        <FaFacebookSquare
                            style={{ backgroundColor: iconcolor }}
                        />
                    </a>
                </div>
                <div className="links">
                    <a
                        href="https://www.instagram.com/thehubaubg/"
                        target="_blank"
                    >
                        <GrInstagram style={{ backgroundColor: iconcolor }} />
                    </a>
                </div>
                <div className="links">
                    <a
                        href="https://www.youtube.com/channel/UChdtBZBvaK9XZurP3GjPDug"
                        target="_blank"
                    >
                        <AiFillYoutube style={{ backgroundColor: iconcolor }} />
                    </a>
                </div>
            </div>
        </div>
    );
};
