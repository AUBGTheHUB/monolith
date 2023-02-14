import React from 'react';

export const JudgesCard = ({ Judge, openNewTab }) => {
    return (
        <div className="judge-card background-color">
            <div className="judge-image">
                <img src={Judge.profilepicture} onClick={openNewTab} />
            </div>
            <div className="judge-link">
                <a href={Judge.sociallink}></a>
            </div>
        </div>
    );
};
