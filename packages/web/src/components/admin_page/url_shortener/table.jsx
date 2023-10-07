import { Alert, Button, Form, OverlayTrigger, Popover, Table } from 'react-bootstrap';
import axios from 'axios';
import { useEffect, useState } from 'react';
import { parseToNewAPI, urlShortenerURL } from '../../../Global';
import UrlRow from './row';
import { updateErrorMessage } from './requests';

const popover = (onUpdate, errorMessage) => {
    return (
        <Popover id="popover-basic">
            <Popover.Header as="h3">Want to update or remove?</Popover.Header>
            <Popover.Body>
                {errorMessage !== undefined ? <Alert variant="warning">{errorMessage}</Alert> : null}
                <UpdateUrlForm onUpdate={onUpdate} />
            </Popover.Body>
        </Popover>
    );
};

const UpdateUrlForm = ({ onUpdate }) => {
    const [newShortenedUrl, setNewShortenedUrl] = useState({});

    const handleChange = e => {
        setNewShortenedUrl({
            ...newShortenedUrl,
            [e.target.name]: e.target.value,
        });
    };

    return (
        <>
            <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Set a url:</Form.Label>
                <Form.Control type="text" placeholder="Paste the url" onChange={handleChange} name="url" />
                <Form.Text className="text-muted">Add the new url you want this endpoint to redirect to</Form.Text>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Set an endpoint:</Form.Label>
                <Form.Control type="text" placeholder="Add the endpoint" onChange={handleChange} name="endpoint" />
                <Form.Text className="text-muted">
                    For example `shorted` if you want it to be thehub-aubg.com/s/shorted
                </Form.Text>
            </Form.Group>

            <Button
                variant="primary"
                onClick={() => {
                    onUpdate(newShortenedUrl);
                }}>
                Add
            </Button>
        </>
    );
};

const UrlsTable = () => {
    const [shortenedUrls, setShortenedUrls] = useState([]);
    const [selected, setSelected] = useState('');
    const [trigger, setTrigger] = useState(0);
    const [errorMessage, setErrorMessage] = useState(undefined);
    const [showAddOverlay, setShowAddOverlay] = useState(false);

    const triggerFetch = () => {
        setTrigger(prev => prev + 1);
    };

    const onUpdate = data => {
        axios(parseToNewAPI(urlShortenerURL), {
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
                updateErrorMessage(err, setErrorMessage);
            });
    };

    useEffect(() => {
        axios(parseToNewAPI(urlShortenerURL), {
            headers: {
                'BEARER-TOKEN': localStorage.getItem('auth_token'),
            },
        })
            .then(res => {
                setShortenedUrls(res.data.urls);
            })
            .catch(() => {
                window.alert('API is not responding!');
            });
    }, [trigger]);

    useEffect(() => {
        if (selected) {
            setShowAddOverlay(false);
        }
    }, [selected]);

    useEffect(() => {
        if (showAddOverlay) {
            setSelected(undefined);
        }
    }, [showAddOverlay]);

    return (
        <>
            <OverlayTrigger show={showAddOverlay} placement="bottom" overlay={popover(onUpdate, errorMessage)}>
                <Button
                    variant="primary"
                    style={{ width: '100vw' }}
                    onClick={() => {
                        setShowAddOverlay(prev => !prev);
                    }}>
                    Create a shortened URL
                </Button>
            </OverlayTrigger>
            <Table style={{ color: 'white' }}>
                <thead>
                    <tr>
                        <th>entry</th>
                        <th>url</th>
                    </tr>
                </thead>
                <tbody>
                    {shortenedUrls.map(item => (
                        <UrlRow
                            endpoint={item.endpoint}
                            url={item.url}
                            key={item.endpoint}
                            selected={selected}
                            setSelected={setSelected}
                            triggerFetch={triggerFetch}
                        />
                    ))}
                </tbody>
            </Table>
        </>
    );
};

export default UrlsTable;
