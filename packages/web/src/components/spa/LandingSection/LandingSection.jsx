import React from 'react';
import styles from './landing_section.module.css';
import { checkBrowserValid } from '../../../Global';

export const LandingSection = () => {
    return (
        <div className={styles['welcome-container']}>
            <div className={styles['welcome-text']}>
                <h1>Welcome to The Hub!</h1>
                <p>
                    We are a group of passionate IT-oriented students who strive to make technological innovation thrive
                    within AUBG and beyond.
                </p>
                <button
                    className={styles['aboutUs-btn']}
                    type="button"
                    onClick={() => {
                        window.location.href = '#team';
                    }}
                    style={{ display: checkBrowserValid() ? '' : 'none' }}>
                    Meet the team
                </button>
            </div>
            <div className="hubzzie">
                <img src="hubzzie.png" className={styles['hubzzie-image']} alt="Hubzzie" />
            </div>
        </div>
    );
};
