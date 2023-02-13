import React from 'react';
import { openNewTab } from '../../../../Global';

export const JudgesCard = ({ Judge }) => {
    return (
        <div className="judge-card background-color">
            <div className="judge-image">
                <img src={Judge.profilepicture} onClick={openNewTab} />
                {/* ^^ returns empty object when onClick bcz it directs to null object url ^^ */}
            </div>
            <div className="judge-link">
                <a href={Judge.sociallink}></a>
            </div>
        </div>
    );
};
