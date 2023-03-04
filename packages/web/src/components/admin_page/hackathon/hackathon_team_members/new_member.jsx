import React from 'react';
import { Form, Button } from 'react-bootstrap';
import { useState } from 'react';
import axios from 'axios';
import { useLocation, useNavigate } from 'react-router-dom';
import Validate, { url } from '../../../../Global';
import InvalidClient from '../../invalid_client';

const AddTeamMember = () => {
    const location = useLocation();
    let team_data = location.state.team_data;
    const history = useNavigate();
    const [formState, setFormState] = useState({
        fullname: '',
        teamnoteam: true,
        teamname: team_data.teamname,
        email: '',
        school: '',
        age: 0,
        location: '',
        aboutus: '',
        previouspart: false,
        partdetails: '',
        experience: false,
        level: '',
        strength: '',
        size: '',
        internship: false,
        jobinterests: '',
        sponsorshare: false,
        newsletter: false,
    });

    const handleInputChange = (e) => {
        const target = e.target;
        const name = target.name;
        const value = (name=='age') ? Number(target.value):target.value;
        setFormState({
            ...formState,
            [name]: (target.type == 'checkbox') ? target.checked : value
        });
    };

    const addNewTeamMember = () => {
        // console.log(formState)
        let teamID = team_data.id;
        delete team_data.id;
        axios({
            method: 'post',
            url: url + '/api/hackathon/members',
            headers: { 'BEARER-TOKEN': localStorage.getItem('auth_token') },
            data: { ...formState }
        })
            // eslint-disable-next-line no-unused-vars
            .then((res) => {
                console.log('New member was added');
                team_data["teammembers"].push(res['data']['data']['data']['InsertedID'])

                axios({
                    method: 'put',
                    url: url + `/api/hackathon/teams/${teamID}`,
                    headers: {
                        'BEARER-TOKEN': localStorage.getItem('auth_token')
                    },
                    data: { ...team_data }
                })
                    // eslint-disable-next-line no-unused-vars
                    .then((res) => {
                        console.log('Member added to the team');
                        history(-1);
                    })
                    .catch((err) => {
                        alert(err['response']['data']['data']['data']);
                    });
            })
            .catch((err) => {
                alert(err['response']['data']['data']['data']);
            });
            
         
    };

    if (Validate()) {
        return (
            <div className="add-member-main-div">
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
                        <Form.Label>Email</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="email"
                            name="email"
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

                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Age</Form.Label>
                        <Form.Control
                            type="number"
                            placeholder="age"
                            name="age"
                            onChange={handleInputChange}
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Location</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="location"
                            name="location"
                            onChange={handleInputChange}
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Heard about us?</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="aboutus"
                            name="aboutus"
                            onChange={handleInputChange}
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Previous Participation?</Form.Label>
                        <Form.Check
                            type="switch"
                            label="TEST"
                            name="previouspart"
                            onChange={handleInputChange}
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Participation Info</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="partdetails"
                            name="partdetails"
                            onChange={handleInputChange}
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Experience</Form.Label>
                        <Form.Check
                            type="switch"
                            label="TEST"
                            name="experience"
                            onChange={handleInputChange}
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Programming Level</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="level"
                            name="level"
                            onChange={handleInputChange}
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Strong Sides</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="strength"
                            name="strength"
                            onChange={handleInputChange}
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Shirt Size</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="size"
                            name="size"
                            onChange={handleInputChange}
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Internship</Form.Label>
                        <Form.Check
                            type="switch"
                            label="TEST"
                            name="internship"
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
                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Sponsor Share</Form.Label>
                        <Form.Check
                            type="switch"
                            label="TEST"
                            name="sponsorshare"
                            onChange={handleInputChange}
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>NewsLetter</Form.Label>
                        <Form.Check
                            type="switch"
                            label="TEST"
                            name="newsletter"
                            onChange={handleInputChange}
                        />
                    </Form.Group>

                    <Button
                        variant="primary"
                        type="button"
                        onClick={addNewTeamMember}
                    >
                        Add new member
                    </Button>
                </Form>
            </div>
        );
    } else {
        return <InvalidClient />;
    }
};

export default AddTeamMember;
