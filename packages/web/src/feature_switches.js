import axios from 'axios';
import { createContext, useState } from 'react';
import { parseToNewAPI, url } from './Global';

// Easily disable sections globally

// The following represent the initial global values of the switches
// These values will be replaced after a successful execution of a fetch
const FEATURE_SWITCHES = {
    jobs: false,
    team: true,
    regForm: false,
};
const featureSwitchesArray = Object.entries(FEATURE_SWITCHES).map(([fswitch, value]) => ({
    switch_id: fswitch,
    is_enabled: value,
}));

export default featureSwitchesArray;

const featureSwitchesURL = `${url}/v2/fswitches`;

export const loadFeatureSwitches = () => {
    const result = axios(parseToNewAPI(featureSwitchesURL), {
        method: 'get',
    })
        .then(res => {
            return res.data.documents;
        })
        .catch(() => {
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
    // eslint-disable-next-line
    const [featureSwitches, setFeatureSwitches] = useState(FEATURE_SWITCHES);
    return <FsContext.Provider value={[featureSwitches, setFeatureSwitches]}>{children}</FsContext.Provider>;
};
