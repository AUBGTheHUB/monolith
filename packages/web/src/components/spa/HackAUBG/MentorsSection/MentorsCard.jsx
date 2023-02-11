import React from 'react';

export const MentorsCard = ({ Mentor }) => {
    return (
        <div className="mentor-card">
            <div className="mentor-image">
                <img src={Mentor.profilepicture} />
            </div>
            <div className="mentor-link">
                <a href={Mentor.sociallink}></a>
            </div>
        </div>
    );
};
