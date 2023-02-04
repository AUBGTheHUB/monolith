import React from 'react';
import './about_section.css';

export const AboutSection = () => {
    return (
        <div className="about-container" id="AboutSection">
            <div className="about-image">
                <img src="../../../../aboutus.jpg" alt="" />
            </div>
            <div className="about-text">
                <h1 className="about-title">About us</h1>
                <p className="about-content">
                    Lorem ipsum dolor sit amet consectetur, adipisicing elit.
                    Eligendi veritatis provident illo beatae saepe quis eos
                    autem dolore. Sunt labore commodi inventore id aut fugiat
                    sed accusamus hic, neque iure?
                </p>
                <p className="about-content">
                    Lorem ipsum dolor sit amet consectetur, adipisicing elit.
                    Eligendi veritatis provident illo beatae saepe quis eos
                    autem dolore. Sunt labore commodi inventore id aut fugiat
                    sed accusamus hic, neque iure?
                </p>
                <p className="about-content">
                    Lorem ipsum dolor sit amet consectetur, adipisicing elit.
                    Eligendi veritatis provident illo beatae saepe quis eos
                    autem dolore. Sunt labore commodi inventore id aut fugiat
                    sed accusamus hic, neque iure?
                </p>
            </div>
        </div>
    );
};
