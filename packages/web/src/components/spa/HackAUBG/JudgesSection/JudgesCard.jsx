import React from 'react';
import { openNewTab } from '../../../../Global';

export const JudgesCard = ({ judge }) => {
    return (
        <div>
            {/* judge image card*/}
            <img
                src={judge.profilepicture}
                onClick={() => {
                    openNewTab(judge.sociallink);
                }}
            />
        </div>
    );
};
