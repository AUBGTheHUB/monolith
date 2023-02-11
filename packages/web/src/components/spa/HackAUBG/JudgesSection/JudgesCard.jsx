import React from 'react';

export const JudgesCard = ({ Judge }) => {
    console.log(Judge);

    return (
        <div className="judges-picture">
            <div className="judge-card">
                <div className="judge-image">
                    <img src={Judge.profilepicture} />
                </div>
                <div className="judge-link">
                    <a href={Judge.sociallink}></a>
                </div>
            </div>
        </div>
    );
};
