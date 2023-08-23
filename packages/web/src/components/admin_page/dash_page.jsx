import React from 'react';
import InvalidClient from './invalid_client';
import Validate from '../../Global';
import landingEntries from './landingEntries.json';
import { LandingCard } from './LandingCard';

const Dash = () => {
    if (Validate()) {
        return (
            <div className="dash">
                <div className="dash-box">
                    {landingEntries.map(entry => (
                        <LandingCard
                            text={entry.text}
                            url={entry.url}
                            description={entry.description}
                            title={entry.title}
                            key={entry.title}
                        />
                    ))}
                </div>
            </div>
        );
    } else {
        return <InvalidClient />;
    }
};

export default Dash;
