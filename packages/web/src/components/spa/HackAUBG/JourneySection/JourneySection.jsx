import React from 'react';
import './journey_section.css';
export const JourneySection = () => {
    const getVerticalLineHeight = () => {
        return document.getElementsByClassName('journey-content').offsetHeight;
    };

    return (
        <div className="journey-section">
            <div className="journey-title">
                <h1>The HackAUBG Journey</h1>
            </div>
            <div className="journey-content">
                <div className="journey-column left">
                    <div className="step top" style={{}}>
                        <div className="left-dot"></div>
                        <h2>Gather a team and register</h2>
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

                        <h2>Gather a team and register</h2>
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
                <div className="journey-column right">
                    <div className="step top">
                        <div className="right-dot"></div>
                        <div>
                            <h2>Gather a team and register</h2>
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
                        <h2>Gather a team and register</h2>
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
