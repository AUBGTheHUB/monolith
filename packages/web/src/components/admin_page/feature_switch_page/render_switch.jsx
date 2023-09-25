/* eslint-disable no-unused-vars */
import React, { useState, useEffect } from 'react';
import { Card, Button } from 'react-bootstrap';
import Validate from '../../../Global';
import { url } from '../../../Global';
import InvalidClient from '../invalid_client';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { parseToNewAPI, featureSwictchesURL } from '../../../Global';
import FeatureRow from './row_switch';
import { OverlayTrigger, Popover, Form, Alert } from 'react-bootstrap';

const popover = (onUpdate, errorMessage) => {
    return (
        <Popover id="popover-basic">
            <Popover.Header as="h3">Want to update or remove?</Popover.Header>
            <Popover.Body>
                {errorMessage !== undefined ? <Alert variant="warning">{errorMessage}</Alert> : null}
                <UpdateSwitch onUpdate={onUpdate} />
            </Popover.Body>
        </Popover>
    );
};

const UpdateSwitch = ({ onUpdate }) => {
    const [newSwitch, setNewSwitch] = useState({
        is_enabled: 'true', // Default value for the dropdown
    });

    const handleChange = e => {
        const { name, value } = e.target;

        setNewSwitch({
            ...newSwitch,
            [name]: value,
        });
    };

    return (
        <>
            <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Set a feature:</Form.Label>
                <Form.Control type="text" placeholder="Paste the url" onChange={handleChange} name="switch_id" />
                <Form.Text className="text-muted">Add a new feature</Form.Text>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Set it to true or false:</Form.Label>
                <Form.Select onChange={handleChange} name="is_enabled" value={newSwitch.is_enabled}>
                    <option value="true">True</option>
                    <option value="false">False</option>
                </Form.Select>
                <Form.Text className="text-muted"></Form.Text>
            </Form.Group>

            <Button
                variant="primary"
                onClick={() => {
                    onUpdate(newSwitch);
                    console.log(newSwitch);
                }}>
                Add
            </Button>
        </>
    );
};

const RenderSwitches = () => {
    const history = useNavigate();
    const [swicthes, setSwitches] = useState([]);
    const [trigger, setTrigger] = useState(0);
    const [selected, setSelected] = useState('');
    const [showAddOverlay, setShowAddOverlay] = useState(false);
    const [errorMessage, setErrorMessage] = useState(undefined);

    const getSwitches = () => {
        axios(parseToNewAPI(featureSwictchesURL), {
            method: 'get',
            url: url + '/v2/fswitches',
        })
            .then(res => {
                setSwitches(res.data.documents);
            })
            .catch(err => {
                console.log(err);
            });
    };

    useEffect(() => {
        getSwitches();
    }, []);

    const triggerFetch = () => {
        setTrigger(prev => prev + 1);
    };

    const onUpdate = data => {
        axios(parseToNewAPI(featureSwictchesURL), {
            headers: {
                'BEARER-TOKEN': localStorage.getItem('auth_token'),
            },
            method: 'put',
            data,
        })
            .then(() => {
                triggerFetch();
                if (errorMessage) {
                    setErrorMessage(undefined);
                }
                setShowAddOverlay(false);
            })
            .catch(err => {
                // updateErrorMessage(err, setErrorMessage);
            });
    };

    const renderSwitch = () => {
        return (
            <>
                <OverlayTrigger show={showAddOverlay} placement="bottom" overlay={popover(onUpdate, errorMessage)}>
                    <Button
                        variant="primary"
                        style={{ width: '100vw' }}
                        onClick={() => {
                            setShowAddOverlay(prev => !prev);
                        }}>
                        Create a Feature Switch
                    </Button>
                </OverlayTrigger>

                {swicthes.map(item => (
                    <FeatureRow
                        switch_id={item.switch_id}
                        is_enabled={item.is_enabled}
                        key={item.switch_id}
                        selected={selected}
                        setSelected={setSelected}
                        triggerFetch={triggerFetch}
                    />
                ))}
            </>
        );
    };

    if (Validate()) {
        return <div className="members-box-add-button">{renderSwitch()}</div>;
    } else {
        return <InvalidClient />;
    }
};

export default RenderSwitches;
