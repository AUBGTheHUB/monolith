import React, { useEffect, useState } from 'react';
import { Card, Button } from 'react-bootstrap';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import InvalidClient from '../../invalid_client';
import Validate, { url } from '../../../../Global';

const RenderTeamMembers = () => {
    const location = useLocation();
    const history = useNavigate();
<<<<<<< HEAD
    const [teamMembers, setTeamMembers] = useState();
    const team_data = location.state.team_data;

    const getTeamMembers = () => {
        axios({
            method: 'get',
            url: url + `/api/hackathon/teams/${team_data.id}`,
            headers: { 'BEARER-TOKEN': localStorage.getItem('auth_token') }
        })
            .then((res) => {
                console.log(res.data.data.data);
                setTeamMembers(res.data.data.data.TeamMembers);
=======
    const [team, setTeam] = useState();
    const team_data = location.state.team_data;

    const getTeamMembers = () => {
        axios({
            method: 'get',
            url: url + `/api/hackathon/teams/${team_data['id']}`,
            headers: { 'BEARER-TOKEN': localStorage.getItem('auth_token') }
        })
            .then((res) => {
                setTeam(res.data.data.data);
>>>>>>> d06cb3e (#310 Fix hackathon teams display and adding functionalities)
            })
            // eslint-disable-next-line no-unused-vars
            .catch((err) => {});
    };

    useEffect(() => {
        getTeamMembers();
    }, []);

    const renderMap = () => {
        if (team) {
            return (
<<<<<<< HEAD
                <div className="members-box">
                    {teamMembers.map((person, index) => (
=======
                <div className="teamMembers-box">
                    {team.TeamMembers.map((person, index) => (
>>>>>>> d06cb3e (#310 Fix hackathon teams display and adding functionalities)
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
                                    {'Email: ' + person['email']}
                                </Card.Text>
                                <Card.Text>
                                    {'Email: ' + person['email']}
                                </Card.Text>
                                <Card.Text>
                                    {'School: ' + person['university']}
                                </Card.Text>
                                <Card.Text>
                                    {'Location: ' + person['location']}
                                </Card.Text>
                                <Card.Text>
                                    {'Programming Level: ' +
                                        person['programminglevel']}
                                </Card.Text>
                                <Card.Text>
                                    {'T-shirt Size: ' + person['shirtsize']}
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
                            {
                                state: {
                                    team_data: team_data
                                }
                            }
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
