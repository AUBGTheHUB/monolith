import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
    // checkBrowserValid,
    url,
} from '../../../Global';
//import { Custom } from 'react-hovering-cards-carousel';
import SampleSlider from './Carousel';
//import { MembersCard } from './MembersCard.old';
import { useMediaQuery } from 'react-responsive';
import style from './members.module.css';

export const MembersSection = () => {
    const [members, setMembers] = useState();
    // eslint-disable-next-line

    const three = useMediaQuery({ query: '(max-width: 1400px)' });
    const two = useMediaQuery({ query: '(max-width: 1000px)' });
    const one = useMediaQuery({ query: '(max-width: 800px)' });
    //const isFoldRes = useMediaQuery({ query: '(max-width: 350px)' });

    const getMembers = () => {
        axios({
            method: 'get',
            url: url + '/api/members',
        })
            .then(res => {
                // let localMembers = [];
                // res.data.data.data.map(member => {
                //     localMembers.push(new Custom(member.profilepicture, <MembersCard prop={member} />));
                // });
                setMembers(res.data.data.data);
            })
            // eslint-disable-next-line no-unused-vars
            .catch(err => {});
    };

    useEffect(() => {
        getMembers();
    }, []);
    if (members) {
        return (
            <>
                <div className={style.test}>
                    <h1 className={style['header-for-container']}>Hubbers</h1>
                    <SampleSlider pictures={members} view={one ? 1 : two ? 2 : three ? 3 : 4} />
                </div>
            </>
        );
    }
};
