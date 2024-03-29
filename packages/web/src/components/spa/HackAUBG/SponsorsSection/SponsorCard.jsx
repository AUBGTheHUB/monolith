import React from 'react';
import { openNewTab } from '../../../../Global';

const SponsorCard = ({ sponsor }) => {
    return (
        <img
            src={sponsor.profilepicture}
            alt={sponsor.name}
            onClick={() => {
                openNewTab(sponsor.sociallink);
            }}
        />
    );
};

export default SponsorCard;
