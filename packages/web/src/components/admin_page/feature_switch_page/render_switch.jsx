/* eslint-disable no-unused-vars */
import React, { useState } from 'react';
import { Card, Button } from 'react-bootstrap';
import Validate from '../../../Global';
import { url } from '../../../Global';
import InvalidClient from '../invalid_client';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const RenderSwitches = () => {
    const history = useNavigate();
    const [swicthes, setSwitches] = useState();

    const getSwitches = () => {
        axios({
            method: 'get',
            url: url + '/v2/fswicthes',
        });
    };

    const renderSwitch = () => {
        return <h1>here</h1>;
    };

    if (Validate()) {
        return <div className="members-box-add-button">{renderSwitch()}</div>;
    } else {
        <InvalidClient />;
    }
};

export default RenderSwitches;
