import { API_URL, FEATURE_SWITCHES, FeatureSwitches } from './constants';

export async function useFetchFeatureSwitches() {
    console.log('From env', API_URL);

    try {
        const headers = new Headers();

        const response = await fetch(`${API_URL}/feature-switches`, {
            method: 'GET',
            headers: headers,
        });

        const data = await response.json();

        data.features.forEach((serverSwitch: { name: string; state: boolean }) => {
            if (serverSwitch.name in FEATURE_SWITCHES) {
                const key = serverSwitch.name as keyof FeatureSwitches;
                FEATURE_SWITCHES[key] = serverSwitch.state;
            }
        });

        return FEATURE_SWITCHES;
    } catch (error) {
        console.error('Error fetching feature switches:', error);
    }
}
