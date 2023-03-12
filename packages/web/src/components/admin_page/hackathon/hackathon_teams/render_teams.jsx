import React from 'react';
import { Card, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useState, useEffect } from 'react';
import { url } from '../../../../Global';
import Validate from '../../../../Global';
import InvalidClient from '../../invalid_client';

const RenderTeams = () => {
    const history = useNavigate();
    const [teams, setTeams] = useState();

    const getTeams = () => {
        axios({
            method: 'get',
            url: url + '/api/hackathon/teams',
            headers: { 'BEARER-TOKEN': localStorage.getItem('auth_token') }
        })
            .then((res) => {
                setTeams(res.data.data.data);
            })
            .catch((err) => {
                console.log(err);
            });
    };

    const renderMap = () => {
        if (teams) {
            console.log(teams)
            return (
                <div className="members-box">
                    {teams.map((team, index) => {
                        return (
                            <Card
                                style={{ width: '18rem' }}
                                key={index}
                                className="member-card"
                            >
                                <Card.Body>
                                    <Card.Title>{team['teamname']}</Card.Title>
                                    <Card.Text>
                                        {team['teammembers'].length}
                                    </Card.Text>
                                    <Button
                                        variant="primary"
                                        onClick={() => {
                                            history(
                                                '/admin/dashboard/hackathon/teams/members',
                                                {
                                                    state: {
                                                        team_data: team
                                                    }
                                                }
                                            );
                                        }}
                                    >
                                        Members
                                    </Button>
                                </Card.Body>
                            </Card>
                        );
                    })}
                </div>
            );
        }
    };

    useEffect(() => {
        getTeams();
    }, []);

    if (Validate()) {
        return (
            <div className="members-box-add-button">
                <Button
                    variant="primary"
                    onClick={() => {
                        history('/admin/dashboard/hackathon/teams/add', {});
                    }}>
                        Add Team
                    </Button>
                    {renderMap()}
            </div>
        );
    } else {
        return <InvalidClient />;
    }
};
export default RenderTeams;
