import React from 'react';
import axios from 'axios';
import { useState } from 'react';
import { useEffect } from 'react';
import { url } from '../../../../Global';
import { JudgesCard } from './JudgesCard';
import './judges_section.css';

export const JudgesSection = () => {
    const [jury, setJury] = useState();

    const getJury = () => {
        axios({
            method: 'get',
            url: url + '/api/jury'
        })
            .then((res) => {
                setJury(res.data.data.data);
            })
            // eslint-disable-next-line
            .catch((err) => {
                // do nothing
            });
    };

    const renderJudges = () => {
        if (jury) {
            return (
                <div className="judges-section-container">
                    <h1>Judges</h1>
                    <div className="judge-container">
                        {jury.map((judge, index) => (
                            <JudgesCard judge={judge} key={index} />
                        ))}
                    </div>
                </div>
            );
        }
        return (
            <div className="hack-coming-soon-container">
                <div className="hack-coming-soon-text">
                    <h1>Judges coming</h1>
                    <h1>soon...</h1>
                </div>
            </div>
        );
    };
    useEffect(() => {
        getJury();
    }, []);
    return <>{renderJudges()}</>;
};

export default JudgesSection;
