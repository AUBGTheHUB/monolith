export type envType = 'DEV' | 'LOCAL' | 'PROD';

const ENV: envType = import.meta.env.VITE_ENV || 'LOCAL';
export const API_URLS = {
    DEV: import.meta.env.VITE_API_URL_DEV,
    LOCAL: import.meta.env.VITE_API_URL_LOCAL,
    PROD: import.meta.env.VITE_API_URL_PROD,
};

export const API_URL = API_URLS[ENV] || API_URLS['LOCAL'];

export const FEATURE_SWITCHES = [
    { name: 'MentorsSwitch', state: false },
    { name: 'JurySwitch', state: false },
    { name: 'SponsorsSwitch', state: false },
    { name: 'RegSwitch', state: false },
    { name: 'isRegTeamsFull', state: false },
];
