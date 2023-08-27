import React from 'react';
import Validate from '../../../Global';
import InvalidClient from '../invalid_client';
import UrlsTable from './table';

const UrlShortener = () => {
    if (Validate()) {
        return <UrlsTable />;
    } else {
        <InvalidClient />;
    }
};

export default UrlShortener;
