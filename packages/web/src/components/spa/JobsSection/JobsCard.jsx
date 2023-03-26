import React from 'react';

export const JobsCard = (props) => {
    const displayDescription = () => {
        var n = 345;
        if (props.description.length > n) {
            while (props.description[n] != ' ') {
                n -= 1;
            }
            return <p>{props.description.slice(0, n)}...</p>;
        }
        return <p>{props.description}</p>;
    };

    return (
        <div className="job-card-content">
            <div className="job-logo">
                <img src={props.logo} />
            </div>
            <div className="job-position">
                <h3>{props.position}</h3>
            </div>
            <div className="job-description">{displayDescription()}</div>

            <div className="job-button">
                <a href={props.link}>Read more</a>
            </div>
        </div>
    );
};
