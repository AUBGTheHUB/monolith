import React from 'react';
import './landing_section.css';
import { checkBrowserValid } from '../../../Global';

export const LandingSection = () => {
    return (
        <div className="welcome-container">
            <div className="welcome-text">
                <h1>Welcome to The Hub!</h1>
                <p>
                    We are a group of passionate IT-oriented students who strive
                    to make technological innovation thrive within AUBG and
                    beyond.
                </p>
                <button
                    className="aboutUs-btn"
                    type="button"
                    onClick={() => {
                        window.location.href = '#team';
                    }}
                    style={{ display: checkBrowserValid() ? '' : 'none' }}
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
