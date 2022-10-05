import React from 'react';

import Validate from '../../../Global';
import InvalidClient from '../invalid_client';
import { url } from '../../../Global';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { Form, Button } from 'react-bootstrap';

const AddArticle = () => {
    const history = useNavigate();

    const [formState, setFormState] = useState({
        title: '',
        banner: '',
        mediumLink: '',
        author: ''
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

    // if page does not redirect, this means bad request

    const addNewArticle = () => {
        axios({
            method: 'post',
            url: url + '/api/article/',
            headers: { BEARER_TOKEN: localStorage.getItem('auth_token') },
            data: { ...formState }
        })
            // eslint-disable-next-line no-unused-vars
            .then((res) => {
                console.log('New Article has been added');
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
                        <Form.Label>Title</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="title"
                            name="title"
                            onChange={handleInputChange}
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Author</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="firstName + lastName"
                            name="author"
                            onChange={handleInputChange}
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Banner</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="drive link"
                            name="banner"
                            onChange={handleInputChange}
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>Medium Link</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="https url point to medium article"
                            name="mediumLink"
                            onChange={handleInputChange}
                        />
                    </Form.Group>

                    <Button
                        variant="primary"
                        type="button"
                        onClick={() => {
                            addNewArticle();
                        }}
                    >
                        Add new Article
                    </Button>
                </Form>
            </div>
        );
    } else {
        return <InvalidClient />;
    }
};

export default AddArticle;
