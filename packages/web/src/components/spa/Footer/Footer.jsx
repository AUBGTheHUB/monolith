import React from 'react';
import './footer.css';
import { FaFacebookSquare } from 'react-icons/fa';
import { GrInstagram } from 'react-icons/gr';
import { AiFillYoutube } from 'react-icons/ai';

export const Footer = ({ color, iconColor, iconBgColor }) => {
    return (
        <div className="footer-container" style={{ backgroundColor: color }}>
            <div className="copyright">
                <p>© 2023 The Hub AUBG. All rights reserved</p>
            </div>
            <div className="social-media">
                <div className="links">
                    <span onClick={()=>{openNewTab("https://facebook.com")}}>
                        {/* <a
                            href="https://www.facebook.com/TheHubAUBG"
                            target="_blank"
                            style={{ backgroundColor: iconBgColor }}
                        > */}
                        
                            <FaFacebookSquare style={{ color: iconColor }} />
                        
                    </span>
                </div>
                <div className="links">
                    <span className="icon-footer">
                        <a
                            href="https://www.facebook.com/TheHubAUBG"
                            target="_blank"
                            style={{ backgroundColor: iconBgColor }}
                        >
                            <GrInstagram style={{ color: iconColor }} />
                        </a>
                    </span>
                </div>
                <div className="links">
                    <span className="icon-footer">
                        <a
                            href="https://www.facebook.com/TheHubAUBG"
                            target="_blank"
                            style={{ backgroundColor: iconBgColor }}
                        >
                            <AiFillYoutube style={{ color: iconColor }} />
                        </a>
                    </span>
                </div>
            </div>
        </div>
    );
};
