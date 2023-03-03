import React, { useEffect, useState } from 'react';
import { Card, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import InvalidClient from '../../invalid_client';
import Validate, { url } from '../../../../Global';

const RenderTeamMembers = () => {
    const history = useNavigate();
    const [teamMembers, setTeamMembers] = useState();

    const getTeamMembers = () => {
        axios({
            method: 'get',
            url: url + '/api/hackathon/teams/members',
            headers: { 'BEARER-TOKEN': localStorage.getItem('auth_token') }
        })
            .then((res) => {
                setTeamMembers(res.data.data.data);
            })
            // eslint-disable-next-line no-unused-vars
            .catch((err) => {});
    };

    useEffect(() => {
        getTeamMembers();
    }, []);

    const renderMap = () => {
        if (teamMembers) {
            return (
                <div className="teamMembers-box">
                    {teamMembers.map((person, index) => (
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
                                <Card.Title>{person['fullname']}</Card.Title>
                                <Card.Text>
                                    {'Team: ' + person['teamname']}
                                </Card.Text>
                                <Card.Text>
                                    {'School: ' + person['school']}
                                </Card.Text>
                                <Button
                                    variant="primary"
                                    onClick={() => {
                                        history(
                                            '/admin/dashboard/hackathon/teams/members/actions',
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
                        history(
                            '/admin/dashboard/hackathon/teams/members/add',
                            {}
                        );
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

export default RenderTeamMembers;
