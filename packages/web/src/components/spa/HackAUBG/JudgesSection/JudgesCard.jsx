import React from 'react';
import { openNewTab } from '../../../../Global';

export const JudgesCard = ({ Judge }) => {
    return (
        <div className="judge-card background-color">
            <div>
                {/* judge-image */}
                <img
                    src={Judge.profilepicture}
                    onClick={() => {
                        openNewTab(Judge.sociallink);
                    }}
                />
            </div>
        </div>
    );
};
