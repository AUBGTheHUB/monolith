import axios from 'axios';
import { useEffect, useState } from 'react';

let url =
    process.env.REACT_APP_API_URL !== undefined // eslint-disable-line
        ? process.env.REACT_APP_API_URL // eslint-disable-line
        : location.origin.replace(':3000', '') + ':8000';

const checkBrowserValid = () => {
    const browsers = [
        'Opera',
        'OPR',
        'Edg',
        'Chrome',
        'Safari',
        'Firefox',
        'Chromium'
        // No IE
    ];

    let isValid = false;

    browsers.forEach((x) => {
        if (navigator.userAgent.indexOf(x) != -1) {
            isValid = true;
        }
    });

    return isValid;
};

const Validate = () => {
    const [validated, setValidated] = useState(false);
    useEffect(() => {
        axios({
            method: 'post',
            url: url + '/api/validate',
            headers: { 'BEARER-TOKEN': localStorage.getItem('auth_token') }
        })
            // eslint-disable-next-line no-unused-vars
            .then((res) => {
                setValidated(true);
            })
            // eslint-disable-next-line no-unused-vars
            .catch((err) => {
                setValidated(false);
            });
    }, []);

    return validated;
};

const checkHashAndScroll = () => {
    let hasHash = !!location.hash;
    if (hasHash) {
        setTimeout(() => {
            document
                .getElementById(location.hash.replace('#', ''))
                .scrollIntoView();
        }, 600);
    }
};

const openNewTab = (url) => {
    window.open(url, '_blank');
};

export { url, checkHashAndScroll, checkBrowserValid, openNewTab };
export default Validate;
/*

    this is how you should handle the validation of the client

        if (Validate()) {
            something something
        } else {
            <InvalidClient/>
        }

*/
