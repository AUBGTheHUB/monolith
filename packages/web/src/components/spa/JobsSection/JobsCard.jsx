import React from 'react';

export const JobsCard = (props) => {
    return (
        <div className="card-content">
            <div className="job-logo">
                <img src={props.logo} />
            </div>
            <div className="job-position">
                <h3>{props.position}</h3>
            </div>
            <div className="job-description">
                <p>{props.description}</p>
            </div>
            <div className="job-button">
                <a href={props.link}>Apply Now</a>
            </div>
        </div>
    );
};
