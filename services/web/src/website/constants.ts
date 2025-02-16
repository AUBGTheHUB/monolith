const ENV: 'DEV' | 'LOCAL' | 'PROD' = import.meta.env.ENV || 'DEV';
export const API_URLS = {
    DEV: import.meta.env.VITE_API_URL_DEV,
    LOCAL: import.meta.env.VITE_API_URL_LOCAL,
    PROD: import.meta.env.VITE_API_URL_PROD,
};

export const API_URL = API_URLS[ENV] || API_URLS['DEV'];

export const FEATURE_SWITCHES = [
    { name: 'MentorsSwitch', defaultValue: false },
    { name: 'JurySwitch', defaultValue: false },
];

export async function useFetchFeatureSwitches() {
    const response = await fetch(`${API_URL}/feature-switches`);
    return response.json();
}
