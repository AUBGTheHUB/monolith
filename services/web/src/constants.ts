const ENV: 'DEV' | 'LOCAL' | 'PROD' = import.meta.env.VITE_ENV || 'DEV';
export const API_URLS = {
    DEV: import.meta.env.VITE_API_URL_DEV,
    LOCAL: import.meta.env.VITE_API_URL_LOCAL,
    PROD: import.meta.env.VITE_API_URL_PROD,
};

export const API_URL = API_URLS[ENV] || API_URLS['DEV'];

export const FEATURE_SWITCHES = [
    { name: 'MentorsSwitch', state: false },
    { name: 'JurySwitch', state: false },
];

export async function useFetchFeatureSwitches() {
    try {
        const response = await fetch(`${API_URL}/feature-switches`);

        const data = await response.json();
        console.log('Server data:', data);

        data.features.forEach((serverSwitch: { name: string; state: boolean }) => {
            const localSwitch = FEATURE_SWITCHES.find((fs) => fs.name === serverSwitch.name);
            if (localSwitch) {
                localSwitch.state = serverSwitch.state;
            }
        });

        console.log(FEATURE_SWITCHES);

        return FEATURE_SWITCHES;
    } catch (error) {
        console.error('Error fetching feature switches:', error);
    }
}

useFetchFeatureSwitches();
