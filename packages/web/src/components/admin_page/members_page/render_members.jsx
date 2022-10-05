import React, { useEffect, useState } from 'react';
import { Card, Button } from 'react-bootstrap';
import Validate from '../../../Global';
import { useNavigate } from 'react-router-dom';
import InvalidClient from '../invalid_client';
import axios from 'axios';
import { url } from '../../../Global';

const RenderMembers = () => {
    const history = useNavigate();
    const [members, setMembers] = useState([]);

    const getMembers = () => {
        axios({
            method: 'get',
            url: url + '/api/members'
        })
            .then((res) => {
                setMembers(res.data.data.data);
            })
            // eslint-disable-next-line no-unused-vars
            .catch((err) => {});
    };

    useEffect(() => {
        getMembers();
    }, []);

    const renderMap = () => {
        if (members) {
            return (
                <div className="members-box">
                    {members.map((person, index) => (
                        <Card
                            style={{ width: '18rem' }}
                            key={index}
                            className="member-card"
                        >
                            <Card.Img
                                variant="top"
                                src={person['profilepicture']}
                            />
                            <Card.Body>
                                <Card.Title>
                                    {person['firstname'] +
                                        ' ' +
                                        person['lastname']}
                                </Card.Title>
                                <Card.Text>
                                    {'Position: ' + person['position']}
                                </Card.Text>
                                <Card.Text>
                                    {'Department: ' + person['department']}
                                </Card.Text>
                                <Button
                                    variant="primary"
                                    onClick={() => {
                                        window.open(person['sociallink']);
                                    }}
                                    className="linkedin-button"
                                >
                                    LinkedIn
                                </Button>
                                <Button
                                    variant="primary"
                                    onClick={() => {
                                        history(
                                            '/admin/dashboard/members/actions',
                                            {
                                                state: {
                                                    member_data: person
                                                }
                                            }
                                        );
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

    if (Validate()) {
        return (
            <div className="members-box-add-button">
                <Button
                    variant="primary"
                    onClick={() => {
                        history('/admin/dashboard/members/add', {});
                    }}
                >
                    Add Member
                </Button>
                {renderMap()}
            </div>
        );
    } else {
        <InvalidClient />;
    }
};

export default RenderMembers;
