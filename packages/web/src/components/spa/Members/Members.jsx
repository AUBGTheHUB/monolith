import React, { useEffect, useState } from 'react';
import './members.css';
import axios from 'axios';
import { url } from '../../../Global';

export const Members = () => {
    const [members, setMembers] = useState([]);

    const getMembers = () => {
        axios({
            method: 'get',
            url: url + '/api/members'
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
                    <div className="members-card" key={index}>
                        <h1>{member.firstname + ' ' + member.lastname}</h1>
                    </div>
                ))}
            </div>
        );
    }
};
