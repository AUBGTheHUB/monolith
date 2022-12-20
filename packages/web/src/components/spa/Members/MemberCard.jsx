import React, { useState } from 'react';
import { useMediaQuery } from 'react-responsive';

export const MemberCard = ({ props, animationClassname = 'hidden' }) => {
    const [hoverOverlay, setHoverOverlay] = useState('hidden');
    const isMobile = useMediaQuery({ query: '(max-width: 900px)' });

    // members-card-hover-overlay is the default css value for the overlay which
    // shows up onMouseEnter

    if (props) {
        return (
            <div
                className={isMobile ? 'members-card mobile' : 'members-card'}
                onMouseEnter={() => {
                    // setHoverOverlay('members-card-hover-overlay');
                    setHoverOverlay(animationClassname);
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
