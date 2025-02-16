import { API_URL, FEATURE_SWITCHES } from './constants';

//   this will be required for dev machine
//   const username = import.meta.env.VITE_DEV_USER;
//   const password = import.meta.env.VITE_DEV_PASS;

export async function useFetchFeatureSwitches() {
    try {
        const headers = new Headers();
        //   this will be required for dev machine
        // headers.set('Authorization', 'Basic ' + btoa(username + ':' + password));
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

        return FEATURE_SWITCHES;
    } catch (error) {
        console.error('Error fetching feature switches:', error);
    }
}
