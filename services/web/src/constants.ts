type envType = 'DEV' | 'LOCAL' | 'PROD';

export const ENV_MODE: envType = import.meta.env.VITE_ENV || 'LOCAL';

export const API_URLS = {
    DEV: 'https://dev.thehub-aubg.com/api/v3',
    LOCAL: 'https://localhost:8080/api/v3',
    PROD: 'https://thehub-aubg.com/api/v3',
};

export const API_URL = API_URLS[ENV_MODE] || API_URLS['LOCAL'];

export const FEATURE_SWITCHES = [
    { name: 'MentorsSwitch', state: false },
    { name: 'JurySwitch', state: false },
    { name: 'SponsorsSwitch', state: false },
    { name: 'RegSwitch', state: false },
    { name: 'isRegTeamsFull', state: false },
];
