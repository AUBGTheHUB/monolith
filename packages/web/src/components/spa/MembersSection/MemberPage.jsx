import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { url } from '../../../Global';
import SampleSlider from './Carousel';
import { useMediaQuery } from 'react-responsive';
import style from './members.module.css';

export const MembersSection = () => {
    const [members, setMembers] = useState();

    const three = useMediaQuery({ query: '(max-width: 1400px)' });
    const two = useMediaQuery({ query: '(max-width: 1000px)' });
    const one = useMediaQuery({ query: '(max-width: 800px)' });

    const getMembers = () => {
        axios({
            method: 'get',
            url: url + '/api/members',
        })
            .then(res => {
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
                <h1 className={style['header-for-container']}>Hubbers</h1>
                <div className={style.test}>
                    <SampleSlider pictures={members} view={one ? 1 : two ? 2 : three ? 3 : 4} />
                </div>
            </>
        );
    }
};
