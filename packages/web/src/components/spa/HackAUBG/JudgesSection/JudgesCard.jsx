import React from 'react';

export const JudgesCard = ({ Judge, handleClick }) => {
    return (
        <div className="judge-card">
            <div className="judge-image">
                <img src={Judge.profilepicture} onClick={handleClick} />
            </div>
            <div className="judge-link">
                <a href={Judge.sociallink}></a>
            </div>
        </div>
    );
};
