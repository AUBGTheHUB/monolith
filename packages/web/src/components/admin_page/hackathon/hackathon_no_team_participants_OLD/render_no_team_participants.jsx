import React, { useEffect, useState } from 'react';
import { Card, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import InvalidClient from '../../invalid_client';
import Validate, { url } from '../../../../Global';

const RenderNoTeamParticipants = () => {
    const history = useNavigate();
    const [teamMembers, setTeamMembers] = useState();

    const getTeamMembers = () => {
        axios({
            method: 'get',
            url: url + '/api/hackathon/participants_no_team',
            headers: { 'BEARER-TOKEN': localStorage.getItem('auth_token') },
        })
            .then(res => {
                setTeamMembers(res.data.data.data);
            })
            // eslint-disable-next-line no-unused-vars
            .catch(err => {
                console.log(err);
            });
    };

    useEffect(() => {
        getTeamMembers();
    }, []);

    const renderMap = () => {
        if (teamMembers) {
            return (
                <div className="members-box">
                    {teamMembers.map((person, index) => (
                        <Card style={{ width: '18rem' }} key={index} className="member-card">
                            <Card.Img variant="top" src={person['profilepicture']} />
                            <Card.Body>
                                <Card.Title>{person['fullname']}</Card.Title>
                                <Card.Text>
                                    <b>Email: </b> {person['email']}
                                </Card.Text>
                                <Card.Text>
                                    <b>School: </b>
                                    {person['university']}
                                </Card.Text>
                                <Card.Text>
                                    <b>Age: </b>
                                    {person['age']}
                                </Card.Text>
                                <Card.Text>
                                    <b>Location: </b>
                                    {person['location']}
                                </Card.Text>
                                <Card.Text>
                                    <b>How they heard about us: </b>
                                    {person['heardaboutus']}
                                </Card.Text>
                                <Card.Text>
                                    <b>Programming Level: </b>
                                    {person['programminglevel']}
                                </Card.Text>
                                <Card.Text>
                                    <b>Strong sides: </b>
                                    {person['strongsides']}
                                </Card.Text>
                                <Card.Text>
                                    <b>Job interests: </b>
                                    {person['jobinterests']}
                                </Card.Text>
                                <Card.Text>
                                    <b>T-shirt Size: </b>
                                    {person['shirtsize']}
                                </Card.Text>
                                <Button
                                    variant="primary"
                                    onClick={() => {
                                        history('/admin/dashboard/hackathon/noteamparticipants/actions', {
                                            state: {
                                                member_data: person,
                                            },
                                        });
                                    }}>
                                    Actions
                                </Button>
                                <Button
                                    variant="success"
                                    onClick={() => {
                                        history('/admin/dashboard/hackathon/teams', {
                                            state: {
                                                member_data: person,
                                            },
                                        });
                                    }}>
                                    Add to team
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
                        history('/admin/dashboard/hackathon/noteamparticipants/add');
                    }}>
                    Add a Participant
                </Button>
                {renderMap()}
            </div>
        );
    } else {
        <InvalidClient />;
    }
};

export default RenderNoTeamParticipants;
