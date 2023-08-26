import { createContext, useState } from 'react';

// Easily disable sections globally

// The following represent the initial global values of the switches
// These values will be replaced after a successful execution of a fetch
const FEATURE_SWITCHES = {
    jobs: false,
    team: true,
    regForm: false,
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
