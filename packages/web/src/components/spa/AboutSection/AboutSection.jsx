import React from 'react';
import './about_section.css';

export const AboutSection = () => {
    return (
        <div className="about-container" id="about">
            <div className="about-image">
                <img src="../../../../aboutus.jpg" alt="" />
            </div>
            <div className="about-text">
                <h1 className="about-title">About us</h1>
                <p className="about-content">
                    The Hub is a community of young and ambitious students with
                    an interest in software development, engineering, design,
                    and technology. Our belief is that getting together with
                    like-minded individuals to exchange experience and ideas is
                    the key ingredient needed to ignite innovation and
                    entrepreneurship into the minds and hearts of fellow
                    enthusiasts. This is what truly motivates us to get
                    together, organize events, and encourage change.
                </p>
            </div>
        </div>
    );
};
