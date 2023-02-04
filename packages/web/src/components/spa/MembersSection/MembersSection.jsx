import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { url } from '../../../Global';
import { Carousel, Custom } from 'react-hovering-cards-carousel';
import { MembersCard } from './MembersCard';
import { useMediaQuery } from 'react-responsive';
import '../ArticlesSection/articles_section.css';git add .

export const MembersSection = () => {
    const [members, setMembers] = useState([]);

    const isMobile = useMediaQuery({ query: '(max-width: 1000px)' });
    const isFoldRes = useMediaQuery({ query: '(max-width: 500px' });

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
                    transform: `scale(${isMobile && !isFoldRes ? 1.18 : 1})`
                }}
            >
                <h1 className="header-for-container">Hubbers</h1>
                {/* <p className="description-for-container">
                    Get ready to meet the dream team behind the University IT
                    Club! Our developers are constantly engaged with carrying
                    out both internal and external projects, while our PR
                    department is dedicated to effectively promoting our brand.
                    Our marketing professionals know how to craft compelling
                    messaging, and our logistics team ensures that everything
                    runs smoothly. Together, there&lsquo;s no challenge we
                    can&lsquo;t tackle. Let&lsquo;s make some amazing things
                    happen!
                </p> */}
                <Carousel cards={members} scale={1.5} buttonSpacing={40} />
            </div>
        </>
    );
};
