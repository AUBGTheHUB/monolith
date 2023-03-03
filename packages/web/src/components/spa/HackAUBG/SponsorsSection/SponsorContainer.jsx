import React from 'react';
import './sponsors_section.css';
import SponsorCard from './SponsorCard';

const SponsorsContainer = ({ sponsors, category }) => {
    if (sponsors.length !== 0) {
        return (
            <>
                <h1
                    style={{
                        color: 'black'
                    }}
                >
                    {category.toUpperCase()}
                </h1>
                <div className={category + '-box'}>
                    <div className="logo-container">
                        {sponsors.map((sponsor, index) => (
                            <SponsorCard sponsor={sponsor} key={index} />
                        ))}
                    </div>
                </div>
            </>
        );
    }
};

export default SponsorsContainer;
