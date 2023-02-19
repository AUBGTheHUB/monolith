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
                    <span className="icon-footer">
                        <a
                            href="https://www.facebook.com/TheHubAUBG"
                            target="_blank"
                            style={{ backgroundColor: iconcolor }}
                        >
                            <FaFacebookSquare />
                        </a>
                    </span>
                </div>
                <div className="links">
                    <span className="icon-footer">
                        <a
                            href="https://www.facebook.com/TheHubAUBG"
                            target="_blank"
                            style={{ backgroundColor: iconcolor }}
                        >
                            <GrInstagram />
                        </a>
                    </span>
                </div>
                <div className="links">
                    <span className="icon-footer">
                        <a
                            href="https://www.facebook.com/TheHubAUBG"
                            target="_blank"
                            style={{ backgroundColor: iconcolor }}
                        >
                            <AiFillYoutube />
                        </a>
                    </span>
                </div>
            </div>
        </div>
    );
};
