import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { url } from '../../../Global';
import { Carousel, Custom } from 'react-hovering-cards-carousel';
import { MembersCard } from './MembersCard';
import '../ArticlesSection/articles_section.css';

export const MembersSection = () => {
    const [members, setMembers] = useState([]);

    const getMembers = () => {
        axios({
            method: 'get',
            url: url + '/api/members'
        })
            .then((res) => {
                let localMembers = [];
                res.data.data.data.map((member) => {
                    localMembers.push(
                        new Custom(
                            member.profilepicture,
                            <MembersCard prop={member} />
                        )
                    );
                });
                setMembers(localMembers);
            })
            // eslint-disable-next-line no-unused-vars
            .catch((err) => {
                console.log(err);
            });
    };

    useEffect(() => {
        getMembers();
    }, []);

    return (
        <>
            <div className="members-section-container">
                <h1 className="header-for-container">Hubbers</h1>
                <Carousel cards={members} scale={1} />
            </div>
        </>
    );
};
