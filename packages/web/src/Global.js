import axios from 'axios';
import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const hasPort = url => {
    const portRegex = /:\d+/;
    return portRegex.test(url);
};

const url = !hasPort(origin) ? origin : origin.replace(/(^[^:]*:[^:]*):.*$/, '$1') + ':8000';

const parseToNewAPI = url => url.replace('8000', '6969');

const objUploaderURL = `${url}/v2/uploader`;
const urlShortenerURL = `${url}/v2/shortener`;
const featureSwitchesURL = parseToNewAPI(`${url}/v2/fswitches`);
const registerURL = parseToNewAPI(`${url}/v2/hackathon/participants`);
const HEADERS = { 'BEARER-TOKEN': localStorage.getItem('auth_token') };

const checkBrowserValid = () => {
    const browsers = [
        'Opera',
        'OPR',
        'Edg',
        'Chrome',
        'Safari',
        'Firefox',
        'Chromium',
        // No IE
    ];

    let isValid = false;

    browsers.forEach(x => {
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
            headers: { 'BEARER-TOKEN': localStorage.getItem('auth_token') },
        })
            // eslint-disable-next-line no-unused-vars
            .then(() => {
                setValidated(true);
            })
            // eslint-disable-next-line no-unused-vars
            .catch(() => {
                setValidated(false);
            });
    }, []);

    return validated;
};

const checkHashAndScroll = () => {
    let hasHash = !!location.hash;
    if (hasHash) {
        setTimeout(() => {
            document.getElementById(location.hash.replace('#', '')).scrollIntoView();
        }, 600);
    }
};

const openNewTab = url => {
    window.open(url, '_blank');
};

const handleUrlDependantStyling = () => {
    let link = document.querySelector("link[rel~='icon']");

    if (!link) {
        link = document.createElement('link');
        link.rel = 'icon';
        document.head.appendChild(link);
    }

    let origin = new URL(location.href).origin;
    let favicon, iosIcon, title;

    if (location.href.includes('hackaubg')) {
        favicon = '/favicon-green.ico';
        iosIcon = '/green-logo512.png';
        title = 'HackAUBG 5.0';
        document.body.style.backgroundColor = '#222222';
    } else {
        favicon = '/favicon.ico';
        iosIcon = '/logo512.png';
        title = 'The Hub AUBG';
        document.body.style.backgroundColor = 'rgb(118, 181, 197)';
    }

    let iconPath = origin + favicon;
    let appleIconPath = origin + iosIcon;
    document.title = title;

    document.querySelector('link[rel="apple-touch-icon"]').href = appleIconPath;
    link.href = iconPath;
};

const History = {
    navigate: null,
    push: (page, ...rest) => History.navigate(page, ...rest),
};

const NavigateSetter = () => {
    History.navigate = useNavigate();

    return null;
};

const navigateTo = endpoint => {
    History.navigate(endpoint);

    document.dispatchEvent(new Event('locationChange'));
};

const goBackIfActionsAreStateless = () => {
    /**
     * @description Fix for https://github.com/AUBGTheHUB/monolith/issues/98
     */

    if (location.href.includes('actions')) {
        const currentLocation = useLocation();
        if (!currentLocation.state) {
            location.href = location.href.replace(/\/[^/]+$/, '');
        }
    }
};

export {
    url,
    checkHashAndScroll,
    checkBrowserValid,
    openNewTab,
    handleUrlDependantStyling,
    NavigateSetter,
    navigateTo,
    objUploaderURL,
    goBackIfActionsAreStateless,
    parseToNewAPI,
    urlShortenerURL,
    featureSwitchesURL,
    registerURL,
    HEADERS,
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
