import React from 'react';
import axios from 'axios';
import { useState } from 'react';
import { useEffect } from 'react';
import { url } from '../../../../Global';
import SimpleSlider from '../Carousel';
import './judges_section.css';

export const JudgesSection = () => {
    const [jury, setJury] = useState();

    const getJury = () => {
        axios({
            method: 'get',
            url: url + '/api/jury',
        })
            .then(res => {
                setJury(res.data.data.data);
            })
            // eslint-disable-next-line
            .catch(err => {
                // do nothing
            });
    };

    const renderJudges = () => {
        if (jury) {
            return (
                <div className="judges-section-container">
                    <img className="pacman-right" src="Pacman-right.png"></img>
                    <h1>Judges</h1>
                    <div className="judge-container">
                        <SimpleSlider pictures={jury} view={4}></SimpleSlider>
                    </div>
                </div>
            );
        }
        return (
            <div className="judges-coming-soon-container">
                <h1>
                    Judges coming <br />
                    soon...
                </h1>
            </div>
        );
    };
    useEffect(() => {
        getJury();
    }, []);
    return <>{renderJudges()}</>;
};

export default JudgesSection;
