import React, { useState } from 'react';

export const MemberCard = ({ props }) => {
    const [hoverOverlay, setHoverOverlay] = useState('hidden');
    return (
        <div
            className="members-card"
            onMouseEnter={() => {
                setHoverOverlay('members-card-hover-overlay');
            }}
            onMouseLeave={() => {
                setHoverOverlay('hidden');
            }}
        >
            <div className={hoverOverlay}>
                <h3>{props.firstname + ' ' + props.lastname}</h3>
            </div>
            <img className="members-card-pfp" src={props.profilepicture} />
        </div>
    );
};
