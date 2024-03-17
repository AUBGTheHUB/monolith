import React, { useEffect, useState } from 'react';
import { Card, Button } from 'react-bootstrap';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import InvalidClient from '../../invalid_client';
import Validate, { url } from '../../../../Global';

const RenderTeamMembers = () => {
    const location = useLocation();
    const history = useNavigate();
    const [teamMembers, setTeamMembers] = useState();
    const team_data = location.state.team_data;
    const [isVerified, setVerified] = useState(false);

    const deleteTeam = () => {
        console.log(team_data['id']);
        axios({
            method: 'delete',
            url: url + `/api/hackathon/teams/${team_data['id']}`,
            headers: { 'BEARER-TOKEN': localStorage.getItem('auth_token') },
        })
            // eslint-disable-next-line no-unused-vars
            .then(res => {
                history(-1);
            })
            // eslint-disable-next-line no-unused-vars
            .catch(err => {});
    };

    const getTeamMembers = () => {
        axios({
            method: 'get',
            url: url + `/api/hackathon/teams/${team_data['id']}`,
            headers: { 'BEARER-TOKEN': localStorage.getItem('auth_token') },
        })
            .then(res => {
                setTeamMembers(res.data.data.data.TeamMembers);
            })
            // eslint-disable-next-line no-unused-vars
            .catch(err => {});
    };

    useEffect(() => {
        getTeamMembers();
    }, []);

    const renderMap = () => {
        if (teamMembers) {
            return (
                <>
                    <Card>
                        <Card.Body>
                            <Card.Title> Team Name: {team_data.teamname}</Card.Title>
                        </Card.Body>
                    </Card>
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
                                            history('/admin/dashboard/hackathon/teams/members/actions', {
                                                state: {
                                                    member_data: person,
                                                },
                                            });
                                        }}>
                                        Actions
                                    </Button>
                                </Card.Body>
                            </Card>
                        ))}
                    </div>
                </>
            );
        }
    };

    if (Validate()) {
        return (
            <div className="members-box-add-button">
                <Button
                    variant="primary"
                    onClick={() => {
                        history('/admin/dashboard/hackathon/teams/members/add', {
                            state: {
                                team_data: team_data,
                            },
                        });
                    }}>
                    Add Member
                </Button>
                {renderMap()}
                <Button
                    variant="success"
                    onClick={() => {
                        history('/admin/dashboard/hackathon/teams/actions', {
                            state: {
                                team_data: team_data,
                            },
                        });
                    }}>
                    EDIT TEAM
                </Button>
                <Button
                    variant="danger"
                    onClick={() => {
                        if (!isVerified) {
                            window.alert(
                                "Are you sure you want to delete this team?\nIf that's the case, press the button again.",
                            );
                            setVerified(true);
                        } else {
                            deleteTeam();
                        }
                    }}>
                    DELETE TEAM
                </Button>
            </div>
        );
    } else {
        <InvalidClient />;
    }
};

export default RenderTeamMembers;
