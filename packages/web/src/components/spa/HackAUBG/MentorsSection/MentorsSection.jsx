import React from 'react';
import axios from 'axios';
import { useState, useEffect } from 'react';
import { url } from '../../../../Global';
import SimpleSlider from '../Carousel';
import './mentors_section.css';
export const MentorsSection = () => {
    const [mentor, setMentors] = useState();
    const getMentors = () => {
        axios({
            method: 'get',
            url: url + '/api/mentors',
        })
            .then(res => {
                setMentors(res.data.data.data);
            })
            // eslint-disable-next-line
            .catch(err => {
                // do nothing
            });
    };

    const renderMentors = () => {
        if (mentor) {
            return (
                <div className="mentors-section-container">
                    <img className="pacman-left" src="Pacman-left.png"></img>
                    <h1>Mentors</h1>
                    <div className="mentor-container">
                        <SimpleSlider pictures={mentor} view={4}></SimpleSlider>
                    </div>
                </div>
            );
        }
        return (
            <div className="mentors-coming-soon-container">
                <h1>
                    Mentors coming <br />
                    soon...
                </h1>
            </div>
        );
    };
    useEffect(() => {
        getMentors();
    }, []);
    return <>{renderMentors()}</>;
};

export default MentorsSection;
