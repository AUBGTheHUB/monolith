import React from 'react';
import './journey_desktop.css';
export const JourneyDesktop = () => {
    const getVerticalLineHeight = () => {
        return document.getElementsByClassName('journey-content').offsetHeight;
    };

    return (
        <div className="journey-desktop-section">
            <div className="journey-desktop-title">
                <h1>The HackAUBG Journey</h1>
            </div>
            <div className="journey-desktop-content">
                <div className="journey-desktop-column left">
                    <div className="step top" style={{}}>
                        <div className="left-dot"></div>
                        <h2>
                            STEP 1:<br></br> Gather a team and register
                        </h2>
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
                    </div>
                    <div className="step bottom">
                        <div className="left-dot"></div>
                        <h2>
                            STEP 3:<br></br> Get Hackathoning
                        </h2>
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
                    </div>
                </div>
                <div
                    className="vertical-line"
                    style={{
                        height: getVerticalLineHeight(),
                        display: 'flex',
                        width: 10
                    }}
                />
                <div className="journey-desktop-column right">
                    <div className="step top">
                        <div className="right-dot"></div>
                        <div>
                            <h2>
                                STEP 2:<br></br> Meet the Hub and prepare
                            </h2>
                            <p>
                                Get together with some fellow enthusiasts and
                                register in the form below! Teams must be
                                between 3 and 6 people. However, if you have
                                less, the Hub team will help you link up with
                                other hackers waiting to participate. If the
                                number of registered teams becomes larger than
                                10, your team will be waitlisted until the last
                                week before the competition.
                            </p>
                        </div>
                    </div>
                    <div className="step bottom">
                        <div className="right-dot"></div>
                        <h2>
                            STEP 4:<br></br> Present and win
                        </h2>
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
                    </div>
                </div>
            </div>
        </div>
    );
};
