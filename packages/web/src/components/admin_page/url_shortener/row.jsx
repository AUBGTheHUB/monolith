import axios from 'axios';
import { OverlayTrigger, Popover, Button, Form, Alert } from 'react-bootstrap';
import { parseToNewAPI, urlShortenerURL } from '../../../Global';
import { useState } from 'react';

const popover = (onDelete, onUpdate, errorMessage) => {
    return (
        <Popover id="popover-basic">
            <Popover.Header as="h3">Want to update or remove?</Popover.Header>
            <Popover.Body>
                {errorMessage !== undefined ? <Alert variant="warning">{errorMessage}</Alert> : null}
                <UpdateUrlForm onUpdate={onUpdate} />
                <Button variant="danger" onClick={onDelete}>
                    Remove
                </Button>
            </Popover.Body>
        </Popover>
    );
};

const HEADERS = { 'BEARER-TOKEN': localStorage.getItem('auth_token') };

const UpdateUrlForm = ({ onUpdate }) => {
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

const UrlRow = ({ endpoint, url, selected, setSelected, triggerFetch }) => {
    const isShown = endpoint === selected;
    const [errorMessage, setErrorMessage] = useState(undefined);

    const onDelete = () => {
        axios(parseToNewAPI(urlShortenerURL + `/${endpoint}`), {
            headers: HEADERS,
            method: 'delete',
        })
            .then(() => {
                triggerFetch();
            })
            .catch(err => {
                const message = err?.response?.data?.message ? err.response.data.message : 'Something went wrong!';
                setErrorMessage(message);
            });
    };

    const onUpdate = newUrl => {
        axios(parseToNewAPI(urlShortenerURL), {
            headers: HEADERS,
            method: 'put',
            data: {
                endpoint,
                url: newUrl,
            },
        })
            .then(() => {
                triggerFetch();
                if (errorMessage) {
                    setErrorMessage(undefined);
                }
            })
            .catch(err => {
                if (err.code === 'ERR_NETWORK') {
                    setErrorMessage('API is not responding!');
                } else if (err?.response?.data?.detail[0]?.ctx?.error) {
                    setErrorMessage('Not a viable URL - ' + err?.response?.data?.detail[0]?.ctx?.error + '!');
                } else {
                    const message = err?.response?.data?.message ? err.response.data.message : 'Something went wrong!';
                    setErrorMessage(message);
                }
            });
    };

    return (
        <>
            <tr>
                <td>https://thehub-aubg.com/s/{endpoint}</td>
                <td>{url}</td>
                <td>
                    <OverlayTrigger show={isShown} placement="left" overlay={popover(onDelete, onUpdate, errorMessage)}>
                        <Button
                            variant="primary"
                            onClick={() => {
                                if (selected === '' || endpoint !== selected) {
                                    setSelected(endpoint);
                                } else {
                                    setSelected('');
                                }
                            }}>
                            Edit
                        </Button>
                    </OverlayTrigger>
                </td>
            </tr>
        </>
    );
};

export default UrlRow;
