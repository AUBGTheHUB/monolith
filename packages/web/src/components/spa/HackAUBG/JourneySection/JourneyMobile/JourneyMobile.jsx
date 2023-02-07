import React from 'react';
import './journey_mobile.css';
import { JourneyStep } from './JourneyStep';
// import { useState } from 'react';

export const JourneyMobile = () => {
    // const [stepTitle, setStepTitle] = useState('container-title-displayed');
    // const [stepContent, setStepContent] = useState(
    //     'container-content-not-displayed'
    // );

    return (
        <div className="journey-mobile-section">
            <div className="journey-mobile-title">
                <h1>The HackAUBG Journey</h1>
            </div>
            <div className="journey-mobile-content">
                <JourneyStep
                    title={<h2>STEP 1: Gather a team and register</h2>}
                    text={
                        <p>
                            Get together with some fellow enthusiasts and
                            register in the form below! Teams must be between 3
                            and 6 people. However, if you have less, the Hub
                            team will help you link up with other hackers
                            waiting to participate. If the number of registered
                            teams becomes larger than 10, your team will be
                            waitlisted until the last week before the
                            competition.
                        </p>
                    }
                />
                <JourneyStep
                    title={<h2>STEP 2: Gather a team and register</h2>}
                    text={
                        <p>
                            Get together with some fellow enthusiasts and
                            register in the form below! Teams must be between 3
                            and 6 people. However, if you have less, the Hub
                            team will help you link up with other hackers
                            waiting to participate. If the number of registered
                            teams becomes larger than 10, your team will be
                            waitlisted until the last week before the
                            competition.
                        </p>
                    }
                />
                <JourneyStep
                    title={<h2>STEP 3: Gather a team and register</h2>}
                    text={
                        <p>
                            Get together with some fellow enthusiasts and
                            register in the form below! Teams must be between 3
                            and 6 people. However, if you have less, the Hub
                            team will help you link up with other hackers
                            waiting to participate. If the number of registered
                            teams becomes larger than 10, your team will be
                            waitlisted until the last week before the
                            competition.
                        </p>
                    }
                />
                <JourneyStep
                    title={<h2>STEP 4: Gather a team and register</h2>}
                    text={
                        <p>
                            Get together with some fellow enthusiasts and
                            register in the form below! Teams must be between 3
                            and 6 people. However, if you have less, the Hub
                            team will help you link up with other hackers
                            waiting to participate. If the number of registered
                            teams becomes larger than 10, your team will be
                            waitlisted until the last week before the
                            competition.
                        </p>
                    }
                />
            </div>
        </div>
    );
};
