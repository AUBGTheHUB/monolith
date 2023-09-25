import { OverlayTrigger, Popover, Button, Form, Alert } from 'react-bootstrap';
import { useState } from 'react';

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

const FeatureRow = ({ switch_id, is_enabled }) => {
    return (
        <div>
            <h1>
                {switch_id} : {String(is_enabled)}
            </h1>
        </div>
    );
};

export default FeatureRow;
