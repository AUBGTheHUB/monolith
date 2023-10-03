/* eslint-disable no-unused-vars */
import React, { useState, useContext } from 'react';
import { Button, Form, OverlayTrigger, Popover, Alert } from 'react-bootstrap';
import axios from 'axios';
import { parseToNewAPI, featureSwitchesURL } from '../../../Global';
import FeatureRow from './row_switch';
import { FsContext } from '../../../feature_switches';

const UpdateSwitch = ({ onUpdate }) => {
    const [newSwitch, setNewSwitch] = useState({
        switch_id: '', // Initialize with an empty string
        is_enabled: true, // Default value for the dropdown as a boolean
    });

    const handleChange = e => {
        const { name, value } = e.target;
        setNewSwitch(prevState => ({
            ...prevState,
            [name]: name === 'is_enabled' ? value === 'true' : value,
        }));
    };

    return (
        <>
            <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Set a feature:</Form.Label>
                <Form.Control
                    type="text"
                    placeholder="Enter new feature switch"
                    onChange={handleChange}
                    name="switch_id"
                    value={newSwitch.switch_id} // Ensure switch_id is controlled
                />
                <Form.Text className="text-muted">Add a new feature</Form.Text>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Set it to true or false:</Form.Label>
                <Form.Select onChange={handleChange} name="is_enabled" value={newSwitch.is_enabled.toString()}>
                    <option value="true">True</option>
                    <option value="false">False</option>
                </Form.Select>
                <Form.Text className="text-muted"></Form.Text>
            </Form.Group>

            <Button
                variant="primary"
                onClick={() => {
                    onUpdate(newSwitch);
                }}>
                Add
            </Button>
        </>
    );
};

export const popover = (onUpdate, errorMessage) => {
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

const updateSwitches = (switches, setSwitches) => data => {
    setSwitches({ ...switches, [data.switch_id]: data.is_enabled });
};

const deleteSwitches = (switches, setSwitches) => switchToRemove => {
    const { [switchToRemove]: _, ...updatedSwitches } = { ...switches };
    setSwitches(updatedSwitches);
};

const RenderSwitches = () => {
    const [selected, setSelected] = useState('');
    const [showAddOverlay, setShowAddOverlay] = useState(false);
    const [errorMessage, setErrorMessage] = useState(undefined);
    const [featureSwitches, setFeatureSwitches] = useContext(FsContext);
    const handleUpdateSwitches = updateSwitches(featureSwitches, setFeatureSwitches);
    const handleDeleteSwitches = deleteSwitches(featureSwitches, setFeatureSwitches);

    const onUpdate = data => {
        const switch_id = data.switch_id;
        const is_enabled = data.is_enabled;

        axios({
            method: 'put',
            url: parseToNewAPI(featureSwitchesURL),
            headers: {
                'BEARER-TOKEN': localStorage.getItem('auth_token'),
            },
            data,
        })
            .then(res => {
                if (errorMessage) {
                    setErrorMessage(undefined);
                }
                setShowAddOverlay(false);
                handleUpdateSwitches({ switch_id, is_enabled });
            })
            .catch(err => {
                // Handle error
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

                {Object.entries(featureSwitches).map(([switch_id, is_enabled]) => (
                    <FeatureRow
                        switch_id={switch_id}
                        is_enabled={is_enabled} // Use the boolean value directly
                        key={switch_id}
                        selected={selected}
                        setSelected={setSelected}
                        triggerFetch={() => {}} // TODO: Remove
                        setFeatureSwitches={setFeatureSwitches}
                        handleDeleteSwitches={handleDeleteSwitches}
                        handleUpdateSwitches={handleUpdateSwitches}
                    />
                ))}
            </>
        );
    };

    return <div className="members-box-add-button">{renderSwitch()}</div>;
};

export default RenderSwitches;
