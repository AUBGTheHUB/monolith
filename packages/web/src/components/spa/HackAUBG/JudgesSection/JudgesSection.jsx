import React from 'react';
import axios from 'axios';
import { useState } from 'react';
import { useEffect } from 'react';
import { url } from '../../../../Global';
import { JudgesCard } from './JudgesCard';
import './judges_section.css';

export const JudgesSection = () => {
    const [jury, setJury] = useState([{}]);

    const getJury = () => {
        axios({
            method: 'get',
            url: url + '/api/jury'
        })
            .then((res) => {
                setJury(res.data.data.data);
            })
            .catch((err) => {
                console.log(err);
            });
    };

    const handleClick = (event) => {
        return () => {
            window.open(event, '_blank', 'noopener noreferrer');
        };
    };

    const renderMap = () => {
        if (jury) {
            return (
                <div className="judges-container">
                    <h1 className="judges-header">Judges</h1>
                    <div className="judges-picture">
                        {jury.map((judge, index) => (
                            <div key={index} className="judge-div">
                                <JudgesCard
                                    Judge={judge}
                                    handleClick={handleClick(judge.sociallink)}
                                />
                            </div>
                        ))}
                    </div>
                </div>
            );
        }
    };
    useEffect(() => {
        getJury();
    }, []);
    return <>{renderMap()}</>;
};

export default JudgesSection;
