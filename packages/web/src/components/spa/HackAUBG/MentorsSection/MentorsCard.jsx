import React from 'react';

export const MentorsCard = ({ Mentor, handleClick }) => {
    return (
        <div className="mentor-card">
            <div className="mentor-image">
                <img src={Mentor.profilepicture} onClick={handleClick} />
            </div>
            <div className="mentor-link">
                <a href={Mentor.sociallink}></a>
            </div>
        </div>
    );
};
