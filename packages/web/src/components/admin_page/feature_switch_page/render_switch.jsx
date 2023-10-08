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
        if (newSwitch.switch_id.trim() === '') {
            toast.error('Please enter switch name');
        } else {
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

const updateSwitches = (switches, setSwitches) => data => {
    setSwitches({ ...switches, [data.switch_id]: data.is_enabled });
};

const deleteSwitches = (switches, setSwitches) => switchToRemove => {
    // eslint-disable-next-line no-unused-vars
    const { [switchToRemove]: _, ...updatedSwitches } = switches; //creates a new object updatedSwitches that is a copy of switches with the siwtchToRemove, removed
    setSwitches(updatedSwitches);
};

const RenderSwitches = () => {
    const [selected, setSelected] = useState('');
    const [showAddOverlay, setShowAddOverlay] = useState(false);
    const [featureSwitches, setFeatureSwitches] = useContext(FsContext);
    const [errorMessage, setErrorMessage] = useState(undefined);
    const handleUpdateSwitches = updateSwitches(featureSwitches, setFeatureSwitches);
    const handleDeleteSwitches = deleteSwitches(featureSwitches, setFeatureSwitches);

    useEffect(() => {
        axios(featureSwitchesURL, {
            method: 'get',
        }).catch(() => {
            toast.error('API IS NOT RESPONDING');
        });
    }, []);

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
                const message = err?.message;
                setErrorMessage(message);
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
            </>
        );
    };

    return <div className="members-box-add-button">{renderSwitch()}</div>;
};

export default RenderSwitches;
