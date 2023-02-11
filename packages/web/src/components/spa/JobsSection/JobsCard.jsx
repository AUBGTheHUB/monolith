import React from 'react';

export const JobsCard = (props) => {
    return (
        <div className="card-info">
            {/* <p>{props.company}</p>
            <p>{props.position}</p>
            <p>{props.description}</p>
            <img src={props.logo} alt="" /> */}
            <div className="general-info">
                <div className="job-logo">
                    <img src={props.logo} />
                </div>
            </div>
            <div className="more-info">
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
        </div>
    );
};
