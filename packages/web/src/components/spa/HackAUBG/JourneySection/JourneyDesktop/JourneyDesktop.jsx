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
                    {stepsData.map((stepData, index) => (
                        <React.Fragment key={stepData.title}>
                            {<img src={`./step-${index + 1}-trail.svg`} id={`step-${index + 1}-trail`} />}
                            <JourneyStep {...stepData} index={index + 1} />
                        </React.Fragment>
                    ))}
                </div>
            </div>
        </>
    );
};
