import React, { useState } from 'react';
import Validate, { gcpToken, objUploaderURL } from '../../../Global';
import { useNavigate } from 'react-router-dom';
import InvalidClient from '../invalid_client';
import { Button, Form } from 'react-bootstrap';
import './s3.css';
import axios from 'axios';

const S3Panel = () => {
    const history = useNavigate();
    const [formState, setFormState] = useState({});
    const [file, setFile] = useState();

    const handleFileSelect = (event) => {
        setFile(event.target.files[0]);
    };

    const addObject = () => {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('filename', formState.filename);

        axios({
            method: 'post',
            url: objUploaderURL,
            headers: {
                Authorization: gcpToken
            },
            data: formData
        })
            // eslint-disable-next-line no-unused-vars
            .then((res) => {
                alert(res['data']['url']);
            })
            .catch((err) => {
                alert(err['response']['data']['message']);
            });
    };

    const handleInputChange = (e) => {
        const target = e.target;
        const value = target.value;
        const name = target.name;

        setFormState({
            ...formState,
            [name]: value
        });
    };

    if (Validate()) {
        return (
            <div className="s3-panel-main">
                <Button
                    variant="primary"
                    onClick={() => {
                        history('/admin/dashboard/s3/objects');
                    }}
                >
                    See All Objects
                </Button>
                <div className="s3-upload-image">
                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>File</Form.Label>
                        <Form.Control
                            type="file"
                            placeholder="upload file"
                            name="file"
                            onChange={handleFileSelect}
                        />
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formBasicText">
                        <Form.Label>File Name</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="come up with a name for the file (e.g. misho_cool_pic)"
                            name="filename"
                            onChange={handleInputChange}
                        />
                    </Form.Group>
                    <Button
                        variant="primary"
                        type="button"
                        onClick={() => {
                            addObject();
                        }}
                    >
                        Add new object
                    </Button>
                </div>
            </div>
        );
    } else {
        <InvalidClient />;
    }
};

export default S3Panel;
