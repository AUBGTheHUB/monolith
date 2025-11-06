export type SeedFeatureSwitch = {
    id: string;
    name: string;
    currentState: boolean;
};

export const seedFeatureSwitches: SeedFeatureSwitch[] = [
    { id: 'fs-1', name: 'New Homepage', currentState: true },
    { id: 'fs-2', name: 'Invite System', currentState: false },
    { id: 'fs-3', name: 'Dark Mode Beta', currentState: false },
    { id: 'fs-4', name: 'Notification Center', currentState: true },
];
