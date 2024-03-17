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
        hasteam: true,
        teamname: member_data.teamname,
        email: '',
        university: '',
        age: 0,
        location: '',
        heardaboutus: '',
        prevhackathonparticipation: false,
        prevhackaubgparticipation: false,
        hasexperience: false,
        programminglevel: '',
        strongsides: '',
        shirtsize: '',
        wantinternship: false,
        jobinterests: '',
        shareinfowithsponsors: false,
        wantjoboffers: false,
    });

    const handleInputChange = e => {
        const target = e.target;
        const name = target.name;
        const value = name == 'age' ? parseInt(target.value) : target.value;
        setFormState({
            ...formState,
            [name]: value,
        });
    };

    // pushing useNavigate -1 otherwise the previously passed state does not get saved (hence auth token)

    const remove_team_member = () => {
        console.log(member_data['id']);
        axios({
            method: 'delete',
            url: url + '/api/hackathon/members/' + member_data['id'],
            headers: { 'BEARER-TOKEN': localStorage.getItem('auth_token') },
        })
            // eslint-disable-next-line no-unused-vars
            .then(res => {
                console.log('Member was deleted');
                history(-1);
            })
            .catch(err => {
                console.log(err);
            });
    };

    const edit_team_member = () => {
        axios({
            method: 'put',
            url: url + '/api/hackathon/members/' + member_data['id'],
            headers: { 'BEARER-TOKEN': localStorage.getItem('auth_token') },
            data: { ...formState },
        })
            // eslint-disable-next-line no-unused-vars
            .then(res => {
                console.log('Member info was edited');
                history(-1);
            })
            .catch(err => {
                console.log(err);
            });
    };

    return (
        <div className="actions-single-member">
            <div className="single-member-box">
                <Card style={{ width: '18rem' }} className="member-card">
                    <Card.Img variant="top" src={member_data['profilepicture']} />
                    <Card.Body>
                        <Card.Title>{member_data['fullname']}</Card.Title>
                        <Card.Text>
                            <b>Team: </b> {member_data['teamname']}
                        </Card.Text>
                        <Card.Text>
                            <b>Email: </b> {member_data['email']}
                        </Card.Text>
                        <Card.Text>
                            <b>School: </b>
                            {member_data['university']}
                        </Card.Text>
                        <Card.Text>
                            <b>Age: </b>
                            {member_data['age']}
                        </Card.Text>
                        <Card.Text>
                            <b>Location: </b>
                            {member_data['location']}
                        </Card.Text>
                        <Card.Text>
                            <b>How they heard about us: </b>
                            {member_data['heardaboutus']}
                        </Card.Text>
                        <Card.Text>
                            <b>Programming Level: </b>
                            {member_data['programminglevel']}
                        </Card.Text>
                        <Card.Text>
                            <b>Strong sides: </b>
                            {member_data['strongsides']}
                        </Card.Text>
                        <Card.Text>
                            <b>Job interests: </b>
                            {member_data['jobinterests']}
                        </Card.Text>
                        <Card.Text>
                            <b>T-shirt Size: </b>
                            {member_data['shirtsize']}
                        </Card.Text>
                        <Button
                            variant="primary"
                            onClick={() => {
                                remove_team_member();
                            }}>
                            Remove
                        </Button>
                    </Card.Body>
                </Card>
            </div>

            <div className="member-form-edit">
                <Form>
                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Full Name</Form.Label>
                        <Form.Control type="text" placeholder="fullname" name="fullname" onChange={handleInputChange} />
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Email</Form.Label>
                        <Form.Control type="text" placeholder="email" name="email" onChange={handleInputChange} />
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>School</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="university"
                            name="university"
                            onChange={handleInputChange}
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Age</Form.Label>
                        <Form.Control type="number" placeholder="age" name="age" onChange={handleInputChange} />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Location</Form.Label>
                        <Form.Control type="text" placeholder="location" name="location" onChange={handleInputChange} />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Heard about us?</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="heardaboutus"
                            name="heardaboutus"
                            onChange={handleInputChange}
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Programming level</Form.Label>
                        <Form.Control
                            type="text"
                            label="programminglevel"
                            name="programminglevel"
                            onChange={handleInputChange}
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Strong Sides</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="strongsides"
                            name="strongsides"
                            onChange={handleInputChange}
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Shirt Size</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="shirtsize"
                            name="shirtsize"
                            onChange={handleInputChange}
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Job Interests</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="jobinterests"
                            name="jobinterests"
                            onChange={handleInputChange}
                        />
                    </Form.Group>
                    <Button
                        variant="primary"
                        type="button"
                        onClick={() => {
                            edit_team_member();
                        }}>
                        Edit member
                    </Button>
                </Form>
            </div>
        </div>
    );
};

export default TeamMemberActions;
