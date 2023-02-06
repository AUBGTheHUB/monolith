import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { url } from '../../../Global';
import { Carousel, Custom } from 'react-hovering-cards-carousel';
import { MembersCard } from './MembersCard';
import { useMediaQuery } from 'react-responsive';
import '../ArticlesSection/articles_section.css';

export const MembersSection = () => {
    const [members, setMembers] = useState([]);

    const isMobile = useMediaQuery({ query: '(max-width: 1000px)' });
    const isFoldRes = useMediaQuery({ query: '(max-width: 350px)' });

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
            <div
                className="members-section-container"
                style={{
                    transform: `scale(${isMobile && !isFoldRes ? 1.1 : 1})`
                }}
            >
                <h1 className="header-for-container">Hubbers</h1>
                <Carousel
                    cards={members}
                    scale={1.25}
                    buttonSpacing={isMobile ? (isFoldRes ? 10 : 30) : 40}
                />
            </div>
        </>
    );
};
