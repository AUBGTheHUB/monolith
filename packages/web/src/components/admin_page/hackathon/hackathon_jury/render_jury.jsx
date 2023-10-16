import React from 'react';
import { Card, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useState } from 'react';
import { useEffect } from 'react';
import { url } from '../../../../Global';
import Validate from '../../../../Global';
import InvalidClient from '../../invalid_client';
import BackBtn from '../../back_button';

const RenderJury = () => {
    const history = useNavigate();
    const [jury, setJury] = useState();

    const getJury = () => {
        axios({
            method: 'get',
            url: url + '/api/jury',
        })
            .then(res => {
                setJury(res.data.data.data);
            })
            .catch(err => {
                console.log(err);
            });
    };

    const renderMap = () => {
        if (jury) {
            return (
                <div className="members-box">
                    {jury.map((jury, index) => (
                        <Card style={{ width: '18rem' }} key={index} className="member-card">
                            <Card.Img variant="top" src={jury['profilepicture']} />
                            <Card.Body>
                                <Card.Title>{jury['firstname'] + ' ' + jury['lastname']}</Card.Title>
                                <Card.Text>{jury['position']}</Card.Text>
                                <Card.Text>{jury['company']}</Card.Text>
                                <Button
                                    variant="primary"
                                    onClick={() => {
                                        window.open(jury['sociallink']);
                                    }}
                                    className="linkedin-button">
                                    LinkedIn
                                </Button>
                                <Button
                                    variant="primary"
                                    onClick={() => {
                                        history('/admin/dashboard/jury/actions', {
                                            state: {
                                                jury_data: jury,
                                            },
                                        });
                                    }}>
                                    Actions
                                </Button>
                            </Card.Body>
                        </Card>
                    ))}
                </div>
            );
        }
    };

    useEffect(() => {
        getJury();
    }, []);

    if (Validate()) {
        return (
            <div className="members-box-add-button">
                <Button
                    variant="primary"
                    onClick={() => {
                        history('/admin/dashboard/jury/add', {});
                    }}>
                    Add Jury
                </Button>
                <BackBtn></BackBtn>
                {renderMap()}
            </div>
        );
    } else {
        <InvalidClient />;
    }
};

export default RenderJury;
