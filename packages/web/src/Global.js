import axios from 'axios';
import { useEffect, useState } from 'react';

// eslint-disable-next-line
const objUploaderURL = process.env.REACT_APP_OBJ_UPLOADER_URL;

// eslint-disable-next-line
const gcpToken = process.env.REACT_APP_GCP_TOKEN;

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

const changeHackFavicon = () => {
    let link = document.querySelector("link[rel~='icon']");

    if (!link) {
        link = document.createElement('link');
        link.rel = 'icon';
        document.head.appendChild(link);
    }

    let origin = new URL(location.href).origin;
    let isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
    let logoPath = isMobile && window.innerWidth < 768 ? (location.href.includes('hackaubg') ? '/green-logo192.png' : '/logo192.png') : (location.href.includes('hackaubg') ? '/green-logo512.png' : '/logo512.png');
    let iconPath = isMobile ? (location.href.includes('hackaubg') ? '/green-logo512.png' : '/logo512.png') : (location.href.includes('hackaubg') ? '/favicon-green.ico' : '/favicon.ico');


    link.href = origin + iconPath;
    document.querySelector('link[rel="apple-touch-icon"]').href = origin + logoPath;
    // link.href = origin + '/favicon-green.ico';
    document.title = 'HackAUBG 5.0';
};

export {
    url,
    checkHashAndScroll,
    checkBrowserValid,
    openNewTab,
    changeHackFavicon,
    objUploaderURL,
    gcpToken
};
export default Validate;
/*

    this is how you should handle the validation of the client

        if (Validate()) {
            something something
        } else {
            <InvalidClient/>
        }

*/
