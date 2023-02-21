import React from 'react';
import { openNewTab } from '../../../../Global';

export const MentorsCard = ({ mentor }) => {
    return (
        <div>
            {/* mentor image card*/}
            <img
                src={mentor.profilepicture}
                onClick={() => {
                    openNewTab(mentor.sociallink);
                }}
            />
        </div>
    );
};
