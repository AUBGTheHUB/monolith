import React from 'react';
import axios from 'axios';
import { useState } from 'react';
import { useEffect } from 'react';
import { url } from '../../../../Global';
import { MentorsCard } from './MentorsCard';
import './mentors_section.css';

export const MentorsSection = () => {
    const [mentor, setMentors] = useState([{}]);

    const getMentors = () => {
        axios({
            method: 'get',
            url: url + '/api/mentors'
        })
            .then((res) => {
                setMentors(res.data.data.data);
            })
            .catch((err) => {
                console.log(err);
            });
    };

    const handleClick = (event) => {
        return () => {
            window.open(event, '_blank', 'thehubaubg');
        };
    };

    const renderMap = () => {
        if (mentor) {
            return (
                <div className="mentors-container">
                    <h1 className="mentors-header">Mentors</h1>
                    <div className="mentors-picture">
                        {mentor.map((mentor, index) => (
                            <div key={index} className="mentors-div">
                                <MentorsCard
                                    Mentor={mentor}
                                    handleClick={handleClick(mentor.sociallink)}
                                />
                            </div>
                        ))}
                    </div>
                </div>
            );
        }
    };
    useEffect(() => {
        getMentors();
    }, []);
    return <>{renderMap()}</>;
};

export default MentorsSection;
