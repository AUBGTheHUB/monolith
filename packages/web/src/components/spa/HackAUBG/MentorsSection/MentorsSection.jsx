import React from 'react';
import axios from 'axios';
import { useState } from 'react';
import { useEffect } from 'react';
import { url } from '../../../../Global';
import { MentorsCard } from './MentorsCard';
import './mentors_section.css';

export const MentorsSection = () => {
    const [mentor, setMentors] = useState();

    const getMentors = () => {
        axios({
            method: 'get',
            url: url + '/api/mentors'
        })
            .then((res) => {
                setMentors(res.data.data.data);
            })
            // eslint-disable-next-line
            .catch((err) => {
                // do nothing
            });
    };

    const renderMentors = () => {
        if (mentor) {
            return (
                <div className="mentors-section-container">
                    <h1>Mentors</h1>
                    <div className="mentor-container">
                        {mentor.map((mentor, index) => (
                            <MentorsCard mentor={mentor} key={index} />
                        ))}
                    </div>
                </div>
            );
        }
    };
    useEffect(() => {
        getMentors();
    }, []);
    return (
        <div className="coming-soon">
            <>{renderMentors()}</>

            <div className="coming-soon-text">
                <h1>Mentors coming</h1>
                <h1>soon...</h1>
            </div>
        </div>
    );
};

export default MentorsSection;
