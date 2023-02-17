import React from 'react';
import { Card, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useState } from 'react';
import { useEffect } from 'react';
import { url } from '../../../../Global';
import Validate from '../../../../Global';
import InvalidClient from '../../invalid_client';

const RenderMentors = () => {
    const history = useNavigate();
    const [mentors, setMentors] = useState();

    const getJobs = () => {
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

    const renderMap = () => {
        if (mentors) {
            return (
                <div className="members-box">
                    {mentors.map((mentor, index) => (
                        <Card
                            style={{ width: '18rem' }}
                            key={index}
                            className="member-card"
                        >
                            <Card.Img
                                variant="top"
                                src={mentor['profilepicture']}
                            />
                            <Card.Body>
                                <Card.Title>
                                    {mentor['firstname'] +
                                        ' ' +
                                        mentor['lastname']}
                                </Card.Title>
                                <Card.Text>{mentor['position']}</Card.Text>
                                <Card.Text>{mentor['company']}</Card.Text>
                                <Button
                                    variant="primary"
                                    onClick={() => {
                                        window.open(mentor['sociallink']);
                                    }}
                                    className="linkedin-button"
                                >
                                    LinkedIn
                                </Button>
                                <Button
                                    variant="primary"
                                    onClick={() => {
                                        history(
                                            '/admin/dashboard/mentors/actions',
                                            {
                                                state: {
                                                    mentor_data: mentor
                                                }
                                            }
                                        );
                                        console.log(mentor['id']);
                                    }}
                                >
                                    Actions
                                </Button>
                            </Card.Body>
                        </Card>
                    ))}
                </div>
            );
        }
    };

    useEffect(() => {
        getJobs();
    }, []);

    if (Validate()) {
        return (
            <div className="members-box-add-button">
                <Button
                    variant="primary"
                    onClick={() => {
                        history('/admin/dashboard/mentors/add', {});
                    }}
                >
                    Add Mentor
                </Button>
                {renderMap()}
            </div>
        );
    } else {
        <InvalidClient />;
    }
};

export default RenderMentors;
