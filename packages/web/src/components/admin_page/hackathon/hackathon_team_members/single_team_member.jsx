import React from 'react';
import { useLocation } from 'react-router-dom';
import { Card, Button, Form } from 'react-bootstrap';
import axios from 'axios';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { url } from '../../../../Global';

const TeamMemberActions = () => {
    const location = useLocation();
    const history = useNavigate();
    const member_data = location.state.member_data;

    const [formState, setFormState] = useState({
        fullname: '',
        teamname: '',
        email: '',
        school: '',
        experiance: '',
        jobinterests: ''
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

    const remove_team_member = () => {
        axios({
            method: 'delete',
            url: url + '/api/dashboard/hackathon/teams/members/' + member_data['id'] + '/',
            headers: { 'BEARER-TOKEN': localStorage.getItem('auth_token') }
        })
            // eslint-disable-next-line no-unused-vars
            .then((res) => {
                console.log('Member was deleted');
                history(-1);
            })
            .catch((err) => {
                console.log(err);
            });
    };

    const edit_team_member = () => {
        axios({
            method: 'put',
            url:
                url +
                '/api/dashboard/hackathon/teams/members/actions/' +
                member_data['id'],
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
                    <Card.Img
                        variant="top"
                        src={member_data['profilepicture']}
                    />
                    <Card.Body>
                        <Card.Title>
                            {member_data['fullname']}
                        </Card.Title>
                        <Card.Text>
                            {'Team: ' + member_data['teamname']}
                        </Card.Text>
                        <Card.Text>
                            {'School: ' + member_data['school']}
                        </Card.Text>
                        <Button
                            variant="primary"
                            onClick={() => {
                                remove_team_member();
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
                        <Form.Label>Full Name</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="fullname"
                            name="fullname"
                            onChange={handleInputChange}
                        />
                    </Form.Group>


                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Team</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="teamname"
                            name="teamname"
                            onChange={handleInputChange}
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>School</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="school"
                            name="school"
                            onChange={handleInputChange}
                        />
                    </Form.Group>

                    <Button
                        variant="primary"
                        type="button"
                        onClick={() => {
                            edit_team_member();
                        }}
                    >
                        Edit member
                    </Button>
                </Form>
            </div>
        </div>
    );
};

export default TeamMemberActions;
