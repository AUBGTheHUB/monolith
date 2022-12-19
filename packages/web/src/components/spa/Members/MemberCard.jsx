import React, { useState } from 'react';

export const MemberCard = ({ props }) => {
    const [hoverOverlay, setHoverOverlay] = useState('hidden');
    if (props) {
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
                    <p>{props.position}</p>
                    <p>{props.department}</p>
                </div>
                <img className="members-card-pfp" src={props.profilepicture} />
            </div>
        );
    }
};
