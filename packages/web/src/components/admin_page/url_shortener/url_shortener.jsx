import React from 'react';
import Validate from '../../../Global';
// import { useNavigate } from 'react-router-dom';
import InvalidClient from '../invalid_client';
import UrlsTable from './table';
// import { Button, Form } from 'react-bootstrap';
// import axios from 'axios';

const UrlShortener = () => {
    if (Validate()) {
        return <UrlsTable />;
    } else {
        <InvalidClient />;
    }
};

export default UrlShortener;
