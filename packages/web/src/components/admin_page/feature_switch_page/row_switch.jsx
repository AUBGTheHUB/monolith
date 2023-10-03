/* eslint-disable no-unused-vars */
/* eslint-disable no-undef */
import { OverlayTrigger, Popover, Button, Form, Alert } from 'react-bootstrap';
import { useState } from 'react';
import { parseToNewAPI, featureSwitchesURL } from '../../../Global';
import axios from 'axios';
import { FsContext } from '../../../feature_switches';
import { updateSwitches } from './render_switch';
import { useContext } from 'react';
import { HEADERS } from '../../../Global';

const popover = (onDelete, onUpdate, errorMessage) => {
    return (
        <Popover id="popover-basic">
            <Popover.Header as="h3">Want to update or remove?</Popover.Header>
            <Popover.Body>
                {errorMessage !== undefined ? <Alert variant="warning">{errorMessage}</Alert> : null}
                <UpdateSwitch onUpdate={onUpdate} />
                <Button variant="danger" onClick={onDelete}>
                    Remove
                </Button>
            </Popover.Body>
        </Popover>
    );
};

const UpdateSwitch = ({ onUpdate }) => {
    const [newFeature, setNewFeature] = useState(undefined);

    const handleChange = e => {
        setNewFeature(e.target.value);
    };

    return (
        <>
            <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Set a new url:</Form.Label>
                <Form.Control type="text" placeholder="Paste the url" onChange={handleChange} />
                <Form.Text className="text-muted">Add the new url you want this endpoint to redirect to</Form.Text>
            </Form.Group>
            <Button
                variant="primary"
                onClick={() => {
                    onUpdate(newFeature);
                }}>
                Update
            </Button>
        </>
    );
};

const FeatureRow = ({ switch_id, is_enabled, selected, setSelected, handleDeleteSwitches, handleUpdateSwitches }) => {
    const isShown = switch_id === selected;
    const [errorMessage, setErrorMessage] = useState(undefined);

    const onDelete = () => {
        axios(parseToNewAPI(featureSwitchesURL + `/${switch_id}`), {
            headers: {
                'BEARER-TOKEN': localStorage.getItem('auth_token'),
            },
            method: 'delete',
        })
            .then(() => {
                handleDeleteSwitches(switch_id);
            })
            .catch(err => {
                const message = err;
                setErrorMessage(message);
            });
    };

    const onUpdate = isEnabled => {
        const is_enabled = JSON.parse(isEnabled);

        axios(parseToNewAPI(featureSwitchesURL), {
            headers: HEADERS,
            method: 'put',
            data: {
                switch_id,
                is_enabled,
            },
        })
            .then(() => {
                if (errorMessage) {
                    setErrorMessage(undefined);
                }
                handleUpdateSwitches({ switch_id, is_enabled });
            })
            .catch(err => {
                updateErrorMessage(err, setErrorMessage);
            });
    };

    return (
        <div>
            <h1>
                {switch_id} : {String(is_enabled)}
                <OverlayTrigger show={isShown} placement="right" overlay={popover(onDelete, onUpdate, errorMessage)}>
                    <Button
                        variant="primary"
                        onClick={() => {
                            if (selected === '' || switch_id !== selected) {
                                setSelected(switch_id);
                            } else {
                                setSelected('');
                            }
                        }}>
                        Edit
                    </Button>
                </OverlayTrigger>
            </h1>
        </div>
    );
};

export default FeatureRow;
