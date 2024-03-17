import React from 'react';
import { Form, Button } from 'react-bootstrap';
import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Validate, { url } from '../../../../Global';
import InvalidClient from '../../invalid_client';

const AddNewTeam = () => {
    const history = useNavigate();

    const [formState, setFormState] = useState({
        teamname: '',
        teammembers: [],
    });

    const handleInputChange = e => {
        const target = e.target;
        const value = target.value;
        const name = target.name;

        setFormState({
            ...formState,
            [name]: value,
        });
    };

    const addNewTeam = () => {
        axios({
            method: 'post',
            url: url + '/api/hackathon/teams/',
            headers: { 'BEARER-TOKEN': localStorage.getItem('auth_token') },
            data: { ...formState },
        })
            // eslint-disable-next-line no-unused-vars
            .then(res => {
                console.log('New team was added');
                history(-1);
            })
            .catch(err => {
                alert(err['response']['data']['data']['data']);
            });
    };

    if (Validate()) {
        return (
            <div className="add-member-main-div">
                <Form>
                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Team Name</Form.Label>
                        <Form.Control type="text" placeholder="teamname" name="teamname" onChange={handleInputChange} />
                    </Form.Group>

                    <Button variant="primary" type="button" onClick={addNewTeam}>
                        Add New Team
                    </Button>
                </Form>
            </div>
        );
    } else {
        return <InvalidClient />;
    }
};

export default AddNewTeam;
