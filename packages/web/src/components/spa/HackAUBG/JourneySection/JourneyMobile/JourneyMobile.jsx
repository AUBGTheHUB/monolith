import React from 'react';
import './journey_mobile.css';
import { JourneyStep } from './JourneyStep';

export const JourneyMobile = () => {
    return (
        <div className="journey-mobile-section">
            <div className="journey-mobile-title">
                <h1>
                    The HackAUBG<br></br> Journey
                </h1>
            </div>
            <div className="journey-mobile-content">
                <JourneyStep
                    title={
                        <h2>
                            STEP 1:<br></br> Gather a team and register
                        </h2>
                    }
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
                    title={
                        <h2>
                            STEP 2:<br></br> Meet the Hub and prepare
                        </h2>
                    }
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
                    title={
                        <h2>
                            STEP 3:<br></br> Get Hackathoning
                        </h2>
                    }
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
                    title={
                        <h2>
                            STEP 4:<br></br> Present and win
                        </h2>
                    }
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
