import React from 'react';
import axios from 'axios';
import { useState } from 'react';
import { useEffect } from 'react';
import { url } from '../../../../Global';
import SimpleSlider from '../Carousel';
import styles from './judges_section.module.css';
import { FsContext } from '../../../../feature_switches';
import { useContext } from 'react';

export const JudgesSection = () => {
    const [jury, setJury] = useState();
    // eslint-disable-next-line
    const [featureSwitches, _] = useContext(FsContext);

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
        if (jury && featureSwitches.Judges) {
            return (
                <div className={styles['judges-section-container']}>
                    <div className={styles['title-container']}>
                        <div className={styles.title}>
                            <h1>Judges</h1>
                        </div>
                        <div className={styles.pac}>
                            <img className={styles['pacman-right']} src="Pacman-right.png"></img>
                        </div>
                    </div>
                    <div className={styles['judge-container']}>
                        <SimpleSlider pictures={jury} view={4}></SimpleSlider>
                    </div>
                </div>
            );
        }
        return (
            <div className={styles['judges-coming-soon-container']}>
                <p>Judges coming soon!</p>
            </div>
        );
    };
    useEffect(() => {
        getJury();
    }, []);
    return <>{renderJudges()}</>;
};

export default JudgesSection;
