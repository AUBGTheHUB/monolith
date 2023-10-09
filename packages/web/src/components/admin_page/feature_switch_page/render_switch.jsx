import React, { useState, useContext, useEffect } from 'react';
import { Button, Form, OverlayTrigger, Popover, Alert } from 'react-bootstrap';
import axios from 'axios';
import { parseToNewAPI, featureSwitchesURL, HEADERS } from '../../../Global';
import FeatureRow from './row_switch';
import { FsContext } from '../../../feature_switches';
import toast from 'react-hot-toast';
import styles from './featureSwitch.module.css';

const UpdateSwitch = ({ onUpdate }) => {
    const [newSwitch, setNewSwitch] = useState({
        switch_id: '',
        is_enabled: true,
    });

    const handleChange = e => {
        const { name, value } = e.target;
        setNewSwitch(prevState => ({
            ...prevState,
            [name]: name === 'is_enabled' ? value === 'true' : value,
        }));
    };

    const handleSubmit = e => {
        e.preventDefault();
        const trimmedSwitchId = newSwitch.switch_id.trim();

        if (trimmedSwitchId === '') {
            toast.error('Please enter switch name');
        } else if (trimmedSwitchId.length > 10) {
            toast.error('Switch name must be 10 characters or less');
        } else {
            newSwitch.switch_id = trimmedSwitchId;
            onUpdate(newSwitch);
        }
    };

    return (
        <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Set a feature:</Form.Label>
                <Form.Control
                    type="text"
                    placeholder="Enter new feature switch"
                    onChange={handleChange}
                    name="switch_id"
                    value={newSwitch.switch_id}
                />
                <Form.Text className="text-muted">Add a new feature</Form.Text>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicIsEnabled">
                <Form.Label>Set it to true or false:</Form.Label>
                <Form.Select onChange={handleChange} name="is_enabled" value={newSwitch.is_enabled.toString()}>
                    <option value="true">True</option>
                    <option value="false">False</option>
                </Form.Select>
                <Form.Text className="text-muted"></Form.Text>
            </Form.Group>

            <Button type="submit" variant="primary">
                Add
            </Button>
        </Form>
    );
};

export const popover = (onUpdate, errorMessage) => {
    return (
        <Popover id="popover-basic">
            <Popover.Header as="h3">Want to update or remove?</Popover.Header>
            <Popover.Body>
                {errorMessage ? <Alert variant="warning">{errorMessage}</Alert> : null}
                <UpdateSwitch onUpdate={onUpdate} />
            </Popover.Body>
        </Popover>
    );
};

// Define a function that updates the "switches" state object by creating a new object.
// The new object includes the existing "switches" data while also updating a specific
// switch's "is_enabled" property based on the provided "data" object.
const updateSwitches = (switches, setSwitches) => data => {
    setSwitches({ ...switches, [data.switch_id]: data.is_enabled });
};

// Define a function to remove a specific switch from the "switches" state.
// Create an updated state object by excluding the specified switch.
// The "_", though unused, is a placeholder for the removed switch.
// Update the state with the new "updatedSwitches" object.
const deleteSwitches = (switches, setSwitches) => switchToRemove => {
    // eslint-disable-next-line no-unused-vars
    const { [switchToRemove]: _, ...updatedSwitches } = switches;
    setSwitches(updatedSwitches);
};

const RenderSwitches = () => {
    //We need to pass the selected switch (switch_id) as a prop to
    //children components in order to maintain state information about whether a switch is currently selected.
    //This allows us to avoid displaying two popovers (menu's for editing or creating switches) at the same time.
    const [selected, setSelected] = useState('');
    const [showAddOverlay, setShowAddOverlay] = useState(false);
    const [featureSwitches, setFeatureSwitches] = useContext(FsContext);
    const [errorMessage, setErrorMessage] = useState(undefined);

    // Create functions to update and delete feature switches and call it by the handleUpdateSwitches/handleDeleteSwitches
    const handleUpdateSwitches = updateSwitches(featureSwitches, setFeatureSwitches);
    const handleDeleteSwitches = deleteSwitches(featureSwitches, setFeatureSwitches);

    //This useEffect is triggered on whenever "selected" state changes (selected is true when we have selected the
    //edit on a certain switch) and if we have selected a switch it hides the showAddOverlay (if opened) for adding new switches
    //Both useEffects serves the purpouse to not have two overlays shown at the same time
    useEffect(() => {
        if (selected) {
            setShowAddOverlay(false);
        }
    }, [selected]);

    //This useEffect is triggered on whenever "showAddOverlay" state changes (showAddOverlay is true when we start creating a new switch)
    //and if we have started making a new switch the selected switch overlay (if opened) for editing existing switches
    //This useEffects serveres the purpouse to not have two overlays shown at the same time
    useEffect(() => {
        if (showAddOverlay) {
            setSelected(undefined);
        }
    }, [showAddOverlay]);

    const onUpdate = data => {
        const switch_id = data.switch_id;
        const is_enabled = data.is_enabled;

        axios({
            method: 'put',
            url: parseToNewAPI(featureSwitchesURL),
            headers: HEADERS,
            data,
        })
            .then(() => {
                if (errorMessage) {
                    setErrorMessage(undefined);
                }
                setShowAddOverlay(false);
                handleUpdateSwitches({ switch_id, is_enabled });
            })
            .catch(err => {
                const message = err?.response?.data?.message;
                setErrorMessage(message);
                toast.error('API IS NOT RESPONDING');
            });
    };

    return (
        <div className="members-box-add-button">
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
            <div className={styles.switches_container}>
                {Object.entries(featureSwitches).map(([switch_id, is_enabled]) => (
                    <FeatureRow
                        switch_id={switch_id}
                        is_enabled={is_enabled}
                        key={switch_id}
                        selected={selected}
                        setSelected={setSelected}
                        handleDeleteSwitches={handleDeleteSwitches}
                        handleUpdateSwitches={handleUpdateSwitches}
                    />
                ))}
            </div>
        </div>
    );
};

export default RenderSwitches;
