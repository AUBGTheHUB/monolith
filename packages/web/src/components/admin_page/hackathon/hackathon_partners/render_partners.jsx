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

const RenderPartners = () => {
    const history = useNavigate();
    const [partners, setPartners] = useState();

    const getPartners = () => {
        axios({
            method: 'get',
            url: url + '/api/partners',
        })
            .then(res => {
                setPartners(res.data.data.data);
            })
            .catch(err => {
                console.log(err);
            });
    };

    const renderMap = () => {
        if (partners) {
            return (
                <div className="members-box">
                    {partners.map((partner, index) => (
                        <Card style={{ width: '18rem' }} key={index} className="member-card">
                            <Card.Img variant="top" src={partner['profilepicture']} />
                            <Card.Body>
                                <Card.Title>{partner['company']}</Card.Title>
                                <Card.Text>{partner['category']}</Card.Text>
                                <Button
                                    variant="primary"
                                    onClick={() => {
                                        window.open(partner['sociallink']);
                                    }}
                                    className="linkedin-button">
                                    Social Link
                                </Button>
                                <Button
                                    variant="primary"
                                    onClick={() => {
                                        history('/admin/dashboard/partners/actions', {
                                            state: {
                                                partner_data: partner,
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
        getPartners();
    }, []);

    if (Validate()) {
        return (
            <div className="members-box-add-button">
                <Button
                    variant="primary"
                    onClick={() => {
                        history('/admin/dashboard/partners/add', {});
                    }}>
                    Add Partners
                </Button>
                <BackBtn></BackBtn>
                {renderMap()}
            </div>
        );
    } else {
        <InvalidClient />;
    }
};

export default RenderPartners;
