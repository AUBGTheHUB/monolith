import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { createFeatureSwitch } from '@/website/AdminPanelPage/DashboardPage/pages/FeatureSwitchesPage/store/useFeatureSwitches';

export default function FeatureSwitchAddPage() {
    const [name, setName] = useState('');
    const [currentState, setCurrentState] = useState(false);
    const [error, setError] = useState<string | null>(null);

    function onSubmit(e: React.FormEvent) {
        e.preventDefault();
        const trimmed = name.trim();
        if (trimmed.length < 2 || trimmed.length > 40) {
            setError('Name must be between 2 and 40 characters.');
            return;
        }
        const id = createFeatureSwitch({ name: trimmed, currentState });
        window.location.assign(`/dashboard/feature-switches/${id}`);
    }

    return (
        <div className="p-6 md:p-8 grid place-items-center">
            <div className="w-full max-w-lg rounded-2xl border p-6">
                <h2 className="text-xl font-semibold text-center mb-6">Add new feature switch</h2>
                <form onSubmit={onSubmit} className="space-y-6">
                    <div>
                        <label className="block text-sm font-medium mb-1">Name</label>
                        <Input
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            maxLength={60}
                            placeholder="FS name"
                        />
                        <div className="text-xs text-gray-500 mt-1">Min 2, max 40 characters.</div>
                        {error && <div className="text-sm text-red-600 mt-1">{error}</div>}
                    </div>

                    <div className="flex items-center justify-between rounded-xl border p-3">
                        <div>
                            <div className="text-sm font-medium">Current State</div>
                            <div className="text-xs text-gray-500">Toggle the feature on/off.</div>
                        </div>
                        <input
                            type="checkbox"
                            checked={currentState}
                            onChange={(e) => setCurrentState(e.target.checked)}
                        />
                    </div>

                    <div className="flex gap-3 justify-center">
                        <a href="/dashboard/feature-switches">
                            <Button variant="outline" type="button">
                                Cancel
                            </Button>
                        </a>
                        <Button type="submit">Add FS</Button>
                    </div>
                </form>
            </div>
        </div>
    );
}
