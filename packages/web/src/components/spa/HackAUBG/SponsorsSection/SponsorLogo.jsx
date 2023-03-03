import React from 'react';
import './sponsors_section.css';

const SponsorLogo = ({ imageSrc, altText }) => {
    return (
        <div className="sponsors-main">
            <img src={imageSrc} alt={altText} />
        </div>
    );
};


export default SponsorLogo;
