import React, { useState, useContext, useEffect } from 'react';
import { Button, Form, OverlayTrigger, Popover, Alert } from 'react-bootstrap';
import axios from 'axios';
import { parseToNewAPI, featureSwitchesURL, HEADERS } from '../../../Global';
import FeatureRow from './row_switch';
import { FsContext } from '../../../feature_switches';
import toast from 'react-hot-toast';
import styles from './featureSwitch.module.css';
import BackBtn from '../back_button';

const handleChange = (e, setNewSwitch) => {
    const { name, value } = e.target;
    setNewSwitch(prevState => ({
        ...prevState,
        [name]: name === 'is_enabled' ? value === 'true' : value,
    }));
};

const handleSubmit = (e, newSwitch, onUpdate) => {
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

const handleChange = (e, setNewSwitch) => {
    const { name, value } = e.target;
    setNewSwitch(prevState => ({
        ...prevState,
        [name]: name === 'is_enabled' ? value === 'true' : value,
    }));
};

const handleSubmit = (e, newSwitch, onUpdate) => {
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

const UpdateSwitch = ({ onUpdate }) => {
    const [newSwitch, setNewSwitch] = useState({
        switch_id: '',
        is_enabled: true,
    });
    return (
        <Form onSubmit={e => handleSubmit(e, newSwitch, onUpdate)}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Label>Set a feature:</Form.Label>
                <Form.Control
                    type="text"
                    placeholder="Enter new feature switch"
                    onChange={e => handleChange(e, setNewSwitch)}
                    name="switch_id"
                    value={newSwitch.switch_id}
                />
                <Form.Text className="text-muted">Add a new feature</Form.Text>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicIsEnabled">
                <Form.Label>Set it to true or false:</Form.Label>
                <Form.Select
                    onChange={e => handleChange(e, setNewSwitch)}
                    name="is_enabled"
                    value={newSwitch.is_enabled.toString()}>
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

/*
    Enable or disable a switch by appending the state of the switch to
    the current state of all switches. If the provided switch is present
    in the state object, it will overwrite its old value with the new one.
    If not, a new entry will be created with the provided id and is_enabled value.
*/
const updateSwitches = (switches, setSwitches) => data => {
    setSwitches({ ...switches, [data.switch_id]: data.is_enabled });
};

/*
    Deletes a switch by desctructuring the state object and extracting
    two variables - one is the switch we want to delete and the other is
    the switches without the switch we want to delete.
    We update the state by passing the new object which excludes
    the soon-to-be considered deleted switch
*/
const deleteSwitches = (switches, setSwitches) => switchToRemove => {
    // eslint-disable-next-line no-unused-vars
    const { [switchToRemove]: _, ...updatedSwitches } = switches;
    setSwitches(updatedSwitches);
};

const onUpdate = (data, errorMessage, setErrorMessage, setShowAddOverlay, handleUpdateSwitches) => {
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
            if (err.code == 'ERR_NETWORK') {
                toast.error('API IS NOT RESPONDING');
            }
        });
};

const RenderSwitches = () => {
    // selected holds the id of the switch which is currently selected for editing
    const [selected, setSelected] = useState('');
    const [showAddOverlay, setShowAddOverlay] = useState(false);
    const [featureSwitches, setFeatureSwitches] = useContext(FsContext);
    const [errorMessage, setErrorMessage] = useState(undefined);

    const handleUpdateSwitches = updateSwitches(featureSwitches, setFeatureSwitches);
    const handleDeleteSwitches = deleteSwitches(featureSwitches, setFeatureSwitches);

    /*
        This useEffect closes opened overlays if there's no currently selected switch
    */
    useEffect(() => {
        if (selected) {
            setShowAddOverlay(false);
        }
    }, [selected]);

    /*
        Remove all currently selected switches if the user opens the menu for creating a new switch.
        This will close all leftover open menus.
    */
    useEffect(() => {
        if (showAddOverlay) {
            setSelected(undefined);
        }
    }, [showAddOverlay]);

    return (
        <div className="members-box-add-button">
            <OverlayTrigger
                show={showAddOverlay}
                placement="bottom"
                overlay={popover(
                    data => onUpdate(data, errorMessage, setErrorMessage, setShowAddOverlay, handleUpdateSwitches),
                    errorMessage,
                )}>
                <Button
                    variant="primary"
                    style={{ width: '100vw' }}
                    onClick={() => {
                        setShowAddOverlay(prev => !prev);
                    }}>
                    Create a Feature Switch
                </Button>
            </OverlayTrigger>
            <BackBtn></BackBtn>
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
