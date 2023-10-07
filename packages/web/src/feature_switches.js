import axios from 'axios';
import { createContext, useState } from 'react';
import { featureSwitchesURL } from './Global';

// Easily disable sections globally

// The following represent the initial global values of the switches
// These values will be replaced after a successful execution of a fetch
const FEATURE_SWITCHES = {
    jobs: false,
    regForm: false,
    team: true,
};

export const loadFeatureSwitches = () => {
    const result = axios(featureSwitchesURL, {
        method: 'get',
    })
        .then(res => {
            return res.data.documents;
        })
        .catch(() => {
            window.alert('API is not responding!');
            return [];
        });

    return result;
};

export const parseFeatureSwitches = featureSwitches => {
    const mappedResult = {};
    featureSwitches.forEach(fs => {
        mappedResult[fs.switch_id] = fs.is_enabled;
    });
    return mappedResult;
};

export const FsContext = createContext();
export const Store = ({ children }) => {
    const [featureSwitches, setFeatureSwitches] = useState(FEATURE_SWITCHES);
    return <FsContext.Provider value={[featureSwitches, setFeatureSwitches]}>{children}</FsContext.Provider>;
};
