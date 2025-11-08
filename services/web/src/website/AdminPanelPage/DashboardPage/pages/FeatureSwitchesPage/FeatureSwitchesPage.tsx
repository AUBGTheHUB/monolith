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
        <div className="min-h-screen grid place-items-center p-6">
            <div className="relative w-full max-w-6xl rounded-[28px] border bg-background p-10 shadow-sm">
                <div className="grid grid-cols-2 gap-10 justify-items-center">
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

                <a
                    href="/dashboard/feature-switches/add"
                    className="absolute bottom-6 right-6 h-12 w-12 rounded-full bg-teal-500 hover:bg-teal-600 grid place-items-center shadow-lg no-underline text-white hover:text-white focus:text-white active:text-white visited:text-white"
                    aria-label="Add feature switch"
                    title="Add feature switch"
                >
                    <span className="text-2xl leading-none text-white">+</span>
                </a>
            </div>
        </div>
    );
}
