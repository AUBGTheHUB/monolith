import React from 'react';
import './sponsors_section.css';

const SponsorCard = ({ sponsor }) => {
    return <img src={sponsor.profilepicture} alt={sponsor.name} />;
};

export default SponsorCard;
