import { OverlayTrigger, Popover, Button, Alert } from 'react-bootstrap';
import { useState } from 'react';
import { parseToNewAPI, featureSwitchesURL } from '../../../Global';
import axios from 'axios';
import './featureSwitch.css';

import { HEADERS } from '../../../Global';

const popover = (onDelete, onUpdate, errorMessage) => {
    return (
        <Popover id="popover-basic">
            <Popover.Header as="h3">Want to update or remove?</Popover.Header>
            <Popover.Body>
                {errorMessage !== undefined ? <Alert variant="warning">{errorMessage}</Alert> : null}
                <Button variant="primary" onClick={onUpdate}>
                    Toggle
                </Button>
                <Button variant="danger" onClick={onDelete}>
                    Remove
                </Button>
            </Popover.Body>
        </Popover>
    );
};

const FeatureRow = ({ switch_id, is_enabled, selected, setSelected, handleDeleteSwitches, handleUpdateSwitches }) => {
    const isShown = switch_id === selected;
    const [errorMessage, setErrorMessage] = useState(undefined);

    const onDelete = () => {
        axios(parseToNewAPI(featureSwitchesURL + `/${switch_id}`), {
            headers: HEADERS,
            method: 'delete',
        })
            .then(() => {
                handleDeleteSwitches(switch_id);
            })
            .catch(err => {
                const message = err?.message;
                setErrorMessage(message);
            });
    };

    const onUpdate = () => {
        const updatedIsEnabled = !is_enabled; // Toggle the value

        axios(parseToNewAPI(featureSwitchesURL), {
            headers: HEADERS,
            method: 'put',
            data: {
                switch_id,
                is_enabled: updatedIsEnabled,
            },
        })
            .then(() => {
                if (errorMessage) {
                    setErrorMessage(undefined);
                }
                handleUpdateSwitches({ switch_id, is_enabled: updatedIsEnabled });
            })
            .catch(err => {
                setErrorMessage(err);
            });
    };

    return (
        <div className="test">
            <p>{switch_id}</p>
            <p>state: {String(is_enabled)}</p>
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
        </div>
    );
};

export default FeatureRow;
