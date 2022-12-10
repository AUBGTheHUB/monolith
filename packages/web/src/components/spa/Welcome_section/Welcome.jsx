import React from 'react';
import './welcome_section.css';

export const Welcome = () => {
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
                    About Us
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
