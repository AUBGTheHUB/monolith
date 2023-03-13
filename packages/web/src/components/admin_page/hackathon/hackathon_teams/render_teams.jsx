import React from 'react';
import { Card, Button } from 'react-bootstrap';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import { useState, useEffect } from 'react';
import { url } from '../../../../Global';
import Validate from '../../../../Global';
import InvalidClient from '../../invalid_client';

const RenderTeams = () => {
    const location = useLocation();
    const history = useNavigate();
    const [teams, setTeams] = useState();
    const member_data = location.state.member_data;

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

    const addParticipantToTeam = (team) => {
        // team.teammembers.push(member_data.id);
        // member_data.hasteam = true;
        // member_data.teamname = team.teamname;
        // console.log(member_data)
        axios({
            method: 'post',
            url:
                url +
                '/api/hackathon/participants_no_team/' +
                member_data.id +
                '/move_to_team/' +
                team.id,
            headers: { 'BEARER-TOKEN': localStorage.getItem('auth_token') },
            data: { member_data }
        })
            .then((res) => {
                console.log(res);
                history(-1);
            })
            .catch((err) => {
                console.log(err);
            });
    };

    const addButton = (team) => {
        if (Object.keys(member_data).length > 0) {
            return (
                <Button
                    variant="success"
                    onClick={() => {
                        console.log(team);
                        addParticipantToTeam(team);
                    }}
                >
                    Add
                </Button>
            );
        }
        return <></>;
    };

    const renderMap = () => {
        if (teams) {
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
                                    {addButton(team)}
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
                    }}
                >
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
