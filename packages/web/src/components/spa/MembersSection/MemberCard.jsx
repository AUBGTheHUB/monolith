import React, { useState } from 'react';
import { useMediaQuery } from 'react-responsive';
import { BsLinkedin } from 'react-icons/bs';

export const MemberCard = ({ props, animationClassname = 'hidden' }) => {
    const [hoverOverlay, setHoverOverlay] = useState('hidden');
    const isMobile = useMediaQuery({ query: '(max-width: 900px)' });

    // members-card-hover-overlay is the default css value for the overlay which
    // shows up on mouse enter
    const NOSYNCDEV = () => {
        if (props.department.toLowerCase().includes('development')) {
            return <p className="NOSYNCDEV">NOSYNCDEV</p>;
        }
    };

    if (props) {
        return (
            <div
                className={isMobile ? 'members-card mobile' : 'members-card'}
                onMouseEnter={() => {
                    setHoverOverlay(animationClassname);
                }}
                onMouseLeave={() => {
                    setHoverOverlay('hidden');
                }}
            >
                <div className={hoverOverlay}>
                    {NOSYNCDEV()}
                    <h3 className="members-card-overlay-text name">
                        {props.firstname + ' ' + props.lastname}
                    </h3>
                    <p className="members-card-overlay-text position">
                        {props.position}
                    </p>
                    {/* <p className="members-card-overlay-text department">
                        {props.department}
                    </p> */}
                    <BsLinkedin
                        className="members-card-overlay-text linkedin-icon"
                        onClick={() => window.open(props.sociallink)}
                    />
                </div>
                <img className="members-card-pfp" src={props.profilepicture} />
            </div>
        );
    }
};
