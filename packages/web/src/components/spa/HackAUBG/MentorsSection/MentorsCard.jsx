import React from 'react';
import { openNewTab } from '../../../../Global';

export const MentorsCard = ({ mentor }) => {
    return (
        <div className="mentor-card">
            <div>
                {/* mentor-image */}
                <img
                    src={mentor.profilepicture}
                    onClick={() => {
                        openNewTab(mentor.sociallink);
                    }}
                />
            </div>
        </div>
    );
};
