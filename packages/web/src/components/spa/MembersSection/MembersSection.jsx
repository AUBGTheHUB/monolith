import React, { useEffect, useState } from 'react';
import './members.css';
import axios from 'axios';
import { url } from '../../../Global';
import { Carousel } from './Carousel';
import { useMediaQuery } from 'react-responsive';
import { MobileCarousel } from './MobileCarousel';

export const MembersSection = () => {
    const [members, setMembers] = useState([]);
    const isMobile = useMediaQuery({ query: '(max-width: 900px)' });

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
        if (!isMobile) {
            return (
                <div className="members-container">
                    <Carousel props={members} />
                </div>
            );
        } else {
            return (
                <div className="members-container">
                    <MobileCarousel props={members} />
                </div>
            );
        }
        // else render Mobile version
        // TBA
    }
};
