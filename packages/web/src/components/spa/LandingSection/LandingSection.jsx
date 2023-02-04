import React from 'react';
import './landing_section.css';

export const LandingSection = () => {
    return (
        <div className="welcome-container">
            <div className="welcome-text">
                <h1>Welcome to The Hub!</h1>
                <p>
                    The IT and innovations club at the American University in
                    Bulgaria.
                </p>
                <button
                    className="aboutUs-btn"
                    type="button"
                    onClick={() => {
                        location.href = '#about';
                    }}
                >
                    Meet the team
                </button>
            </div>
            <div className="hubzzie">
                <img
                    src="hubzzie.png"
                    className="hubzzie-image"
                    alt="Hubzzie"
                />
            </div>
        </div>
    );
};
