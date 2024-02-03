import React from 'react';
import './journey_desktop.css';
import stepsData from '../data.json';
import { JourneyStep } from './JourneyStep';

export const JourneyDesktop = () => {
    return (
        <>
            <div className="journey-desktop-section">
                <div className="journey-desktop-title">
                    <h1>The HackAUBG Journey</h1>
                </div>
                <div className="journey-desktop-content">
                    {stepsData.map(stepData => (
                        <JourneyStep props={stepData} key={stepData.title} />
                    ))}
                </div>
            </div>
        </>
    );
};
