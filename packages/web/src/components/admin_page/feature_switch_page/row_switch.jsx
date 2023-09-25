/* eslint-disable no-undef */
import { OverlayTrigger, Popover, Button, Form, Alert } from 'react-bootstrap';
import { useState } from 'react';
import { parseToNewAPI, featureSwictchesURL } from '../../../Global';
import axios from 'axios';

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

const HEADERS = { 'BEARER-TOKEN': localStorage.getItem('auth_token') };

const UpdateSwitch = ({ onUpdate }) => {
    const [newUrl, setNewUrl] = useState(undefined);

    const handleChange = e => {
        setNewUrl(e.target.value);
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
                    onUpdate(newUrl);
                }}>
                Update
            </Button>
        </>
    );
};

const FeatureRow = ({ switch_id, is_enabled, selected, setSelected, triggerFetch }) => {
    const isShown = switch_id === selected;
    const [errorMessage, setErrorMessage] = useState(undefined);

    const onDelete = () => {
        axios(parseToNewAPI(featureSwictchesURL + `/${switch_id}`), {
            headers: HEADERS,
            method: 'delete',
        })
            .then(() => {
                triggerFetch();
            })
            // eslint-disable-next-line no-unused-vars
            .catch(err => {
                const message = err;
                setErrorMessage(message);
            });
    };

    const onUpdate = newSwitch => {
        axios(parseToNewAPI(featureSwictchesURL), {
            headers: HEADERS,
            method: 'put',
            data: {
                switch_id,
                is_enabled: newSwitch,
            },
        })
            .then(() => {
                triggerFetch();
                if (errorMessage) {
                    setErrorMessage(undefined);
                }
            })
            .catch(err => {
                updateErrorMessage(err, setErrorMessage);
            });
    };

    return (
        <div>
            <h1>
                {switch_id} : {String(is_enabled)}
                <OverlayTrigger show={isShown} placement="left" overlay={popover(onDelete, onUpdate, errorMessage)}>
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
