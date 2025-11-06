import { useState } from 'react';
import FeatureSwitchCard from '@/components/ui/FeatureSwitchCard';
import {
    getAllFeatureSwitches,
    updateFeatureSwitch,
    deleteFeatureSwitch,
    toggleFeatureSwitch,
    type FeatureSwitch,
} from '@/website/AdminPanelPage/DashboardPage/pages/FeatureSwitchesPage/store/useFeatureSwitches';

export default function FeatureSwitchesPage() {
    const [items, setItems] = useState<FeatureSwitch[]>(getAllFeatureSwitches());

    function refresh() {
        setItems(getAllFeatureSwitches());
    }

    return (
        <div className="p-6 md:p-8">
            <div className="mb-6">
                <h1 className="text-2xl font-semibold">Feature switches</h1>
                <p className="text-gray-500">Create, toggle and manage features for thehub-aubg.com</p>
            </div>

            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                {items.map((it: FeatureSwitch) => (
                    <FeatureSwitchCard
                        key={it.id}
                        id={it.id}
                        name={it.name}
                        currentState={it.currentState}
                        onRename={(name) => {
                            updateFeatureSwitch(it.id, { name });
                            refresh();
                        }}
                        onToggle={() => {
                            toggleFeatureSwitch(it.id);
                            refresh();
                        }}
                        onDelete={() => {
                            deleteFeatureSwitch(it.id);
                            refresh();
                        }}
                    />
                ))}
            </div>

            {/* FAB */}
            <a
                href="/dashboard/feature-switches/add"
                className="fixed bottom-6 right-6 h-12 w-12 rounded-full bg-primary text-primary-foreground grid place-items-center shadow-lg text-2xl"
                aria-label="Add feature switch"
            >
                +
            </a>
        </div>
    );
}
