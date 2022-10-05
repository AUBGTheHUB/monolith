import React from 'react';
import { Card, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useState } from 'react';
import { useEffect } from 'react';
import { url } from '../../../../Global';
import Validate from '../../../../Global';
import InvalidClient from '../../invalid_client';

const RenderSponsors = () => {
    const history = useNavigate();
    const [sponsors, setSponsors] = useState([{}]);

    const getJobs = () => {
        axios({
            method: 'get',
            url: url + '/api/sponsors'
        })
            .then((res) => {
                setSponsors(res.data.data.data);
            })
            .catch((err) => {
                console.log(err);
            });
    };

    const renderMap = () => {
        if (sponsors) {
            return (
                <div className="members-box">
                    {sponsors.map((sponsor, index) => (
                        <Card
                            style={{ width: '18rem' }}
                            key={index}
                            className="member-card"
                        >
                            <Card.Img
                                variant="top"
                                src={sponsor['profilepicture']}
                            />
                            <Card.Body>
                                <Card.Title>{sponsor['company']}</Card.Title>
                                <Button
                                    variant="primary"
                                    onClick={() => {
                                        window.open(sponsor['sociallink']);
                                    }}
                                    className="linkedin-button"
                                >
                                    Social Link
                                </Button>
                                <Button
                                    variant="primary"
                                    onClick={() => {
                                        history(
                                            '/admin/dashboard/sponsors/actions',
                                            {
                                                state: {
                                                    sponsor_data: sponsor
                                                }
                                            }
                                        );
                                    }}
                                >
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
        getJobs();
    }, []);

    if (Validate()) {
        return (
            <div className="members-box-add-button">
                <Button
                    variant="primary"
                    onClick={() => {
                        history('/admin/dashboard/sponsors/add', {});
                    }}
                >
                    Add Sponsor
                </Button>
                {renderMap()}
            </div>
        );
    } else {
        <InvalidClient />;
    }
};

export default RenderSponsors;
