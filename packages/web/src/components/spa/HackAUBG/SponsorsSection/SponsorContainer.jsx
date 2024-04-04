import React from 'react';
import SponsorCard from './SponsorCard';
import './sponsors_section.css';

const SponsorsContainer = ({ sponsors, category }) => {
    if (sponsors && sponsors.length !== 0) {
        return (
            <div className={category + '-box'}>
                <div className="logo-container">
                    {sponsors.map((sponsor, index) => (
                        <SponsorCard sponsor={sponsor} key={index} />
                    ))}
                </div>
            </div>
        );
    }
};

export default SponsorsContainer;
