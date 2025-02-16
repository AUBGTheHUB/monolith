import { API_URL, FEATURE_SWITCHES } from './constants';

export async function useFetchFeatureSwitches() {
    try {
        const username = import.meta.env.VITE_DEV_USER;
        const password = import.meta.env.VITE_DEV_PASS;
        const headers = new Headers();
        headers.set('Authorization', 'Basic ' + btoa(username + ':' + password));

        const response = await fetch(`${API_URL}/feature-switches`, {
            method: 'GET',
            headers: headers,
        });

        const data = await response.json();

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
