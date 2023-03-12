import React from 'react';
import { Form, Button } from 'react-bootstrap';
import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Validate, { url } from '../../../../Global';
import InvalidClient from '../../invalid_client';

const AddTeamMember = () => {
    const history = useNavigate();

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

    const addNewTeamMember = () => {
        axios({
            method: 'post',
            url: url + '/api/dasboard/hackathon/teams/members/add',
            headers: { 'BEARER-TOKEN': localStorage.getItem('auth_token') },
            data: { ...formState }
        })
            // eslint-disable-next-line no-unused-vars
            .then((res) => {
                console.log('New member was added');
                history(-1);
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
                            addNewTeamMember();
                        }}
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
