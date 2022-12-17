import React, { useEffect, useState } from 'react';
import './members.css';
import axios from 'axios';

export const Members = () => {
    const [members, setMembers] = useState([]);
    const [hoverOverlay, setHoverOverlay] = useState('hidden');

    const getMembers = () => {
        axios({
            method: 'get',
            url: '/api/members'
        })
            .then((res) => {
                setMembers(res.data.data.data);
            })
            // eslint-disable-next-line no-unused-vars
            .catch((err) => {});
    };

    useEffect(() => {
        getMembers();
    }, []);

    if (members) {
        return (
            <div className="members-container">
                {members.map((member, index) => (
                    <div
                        className="members-card"
                        key={index}
                        onPointerEnter={() => {
                            setHoverOverlay('members-card-hover-overlay');
                        }}
                        onPointerLeave={() => {
                            setHoverOverlay('hidden');
                        }}
                    >
                        <div className={hoverOverlay} />
                        <img src={member.profilePicture} />
                    </div>
                ))}
            </div>
        );
    }
};
