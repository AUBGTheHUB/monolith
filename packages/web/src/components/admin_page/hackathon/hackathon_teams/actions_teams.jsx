import React from 'react';
import { useLocation } from 'react-router-dom';
import { Card, Button, Form } from 'react-bootstrap';
import axios from 'axios';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { url } from '../../../../Global';

const TeamActions = () => {
    const location = useLocation();
    const history = useNavigate();
    const team_data = location.state.team_data;
    console.log(team_data);
    const [formState, setFormState] = useState({
        teamname: '',
        teammembers: team_data.teammembers
    });

    const handleInputChange = (e) => {
        const target = e.target;
        const value = target.value;
        const name = target.name;

        setFormState({
            ...formState,
            [name]: value
        });
    };

    // pushing useNavigate -1 otherwise the previously passed state does not get saved (hence auth token)

    const delete_team = () => {
        axios({
            method: 'delete',
            url: url + '/api/hackathon/teams/' + team_data['id'] + '/',
            headers: { 'BEARER-TOKEN': localStorage.getItem('auth_token') }
        })
            // eslint-disable-next-line no-unused-vars
            .then((res) => {
                console.log('Team was deleted');
                history(-2);
            })
            .catch((err) => {
                console.log(err);
            });
    };

    const edit_team = () => {
        axios({
            method: 'put',
            url: url + '/api/hackathon/teams/' + team_data['id'],
            headers: { 'BEARER-TOKEN': localStorage.getItem('auth_token') },
            data: { ...formState }
        })
            // eslint-disable-next-line no-unused-vars
            .then((res) => {
                console.log('Member info was edited');
                history(-1);
            })
            .catch((err) => {
                console.log(err);
            });
    };

    return (
        <div className="actions-single-member">
            <div className="single-member-box">
                <Card style={{ width: '18rem' }} className="member-card">
                    <Card.Img variant="top" src={team_data['profilepicture']} />
                    <Card.Body>
                        <Card.Title>{team_data['teamname']}</Card.Title>
                        <Card.Text>
                            <b>Team Name: </b> {team_data['teamname']}
                        </Card.Text>
                        <Button
                            variant="primary"
                            onClick={() => {
                                delete_team();
                            }}
                        >
                            Remove
                        </Button>
                    </Card.Body>
                </Card>
            </div>

            <div className="member-form-edit">
                <Form>
                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Team Name</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="teamname"
                            name="teamname"
                            onChange={handleInputChange}
                        />
                    </Form.Group>

                    <Button
                        variant="primary"
                        type="button"
                        onClick={() => {
                            edit_team();
                        }}
                    >
                        Edit member
                    </Button>
                </Form>
            </div>
        </div>
    );
};

export default TeamActions;
