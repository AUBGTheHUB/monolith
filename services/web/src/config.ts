import { useEffect, useState } from 'react';
import { API_URL, FEATURE_SWITCHES as defaultSwitches, FeatureSwitchesType } from './constants';

export function useFeatureSwitches() {
    const [featureSwitches, setFeatureSwitches] = useState<FeatureSwitchesType>(defaultSwitches);

    useEffect(() => {
        async function fetchSwitches() {
            try {
                const response = await fetch(`${API_URL}/feature-switches`);
                const data = await response.json();
                // Create a copy of the default switches
                const updatedSwitches = { ...defaultSwitches };

                // Update only if the feature exists in the defaults
                data.features.forEach((serverSwitch: { name: string; state: boolean }) => {
                    if (serverSwitch.name in updatedSwitches) {
                        const key = serverSwitch.name as keyof FeatureSwitchesType;
                        updatedSwitches[key] = serverSwitch.state;
                    }
                });
                console.log(updatedSwitches);

                setFeatureSwitches(updatedSwitches);
            } catch (error) {
                console.error('Error fetching feature switches:', error);
            }
        }

        fetchSwitches();
    }, []);

    return featureSwitches;
}
