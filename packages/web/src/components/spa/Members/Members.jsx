import React, { useEffect, useState } from 'react';
import './members.css';
import axios from 'axios';
import { url } from '../../../Global';
import { MemberCard } from './MemberCard';

export const Members = () => {
    const [members, setMembers] = useState([]);
    // const [hoverOverlay, setHoverOverlay] = useState('hidden');

    const getMembers = () => {
        axios({
            method: 'get',
            url: url + '/api/members'
        })
            .then((res) => {
                setMembers(res.data.data.data);
            })
            // eslint-disable-next-line no-unused-vars
            .catch((err) => {
                console.log(err);
            });
    };

    useEffect(() => {
        getMembers();
    }, []);

    if (members) {
        return (
            <div className="members-container">
                {members.map((member, index) => (
                    <MemberCard props={member} key={index} />
                ))}
            </div>
        );
    }
};
