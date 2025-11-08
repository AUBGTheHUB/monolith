import { useState } from 'react';
import { Input } from '@/components/ui/input';
import { createFeatureSwitch } from '@/website/AdminPanelPage/DashboardPage/pages/FeatureSwitchesPage/store/useFeatureSwitches';

export default function FeatureSwitchAddPage() {
    const [name, setName] = useState('');
    const [dbKey, setDbKey] = useState('');
    const [errors, setErrors] = useState<{ name?: string; dbKey?: string }>({});

    function validate(): boolean {
        const e: { name?: string; dbKey?: string } = {};
        const n = name.trim();
        const k = dbKey.trim();
        if (n.length < 2 || n.length > 40) e.name = 'Name must be 2–40 characters.';
        if (!/^[a-z0-9_-]{2,40}$/.test(k)) e.dbKey = 'DB Key must be 2–40 chars: a-z, 0-9, _ or -.';
        setErrors(e);
        return Object.keys(e).length === 0;
    }

    function onSubmit(e: React.FormEvent) {
        e.preventDefault();
        if (!validate()) return;
        createFeatureSwitch({ name: name.trim(), dbKey: dbKey.trim(), currentState: false });
        window.location.assign('/dashboard/feature-switches');
    }

    const outlineBtn =
        'px-4 py-2 rounded-md border border-slate-300 bg-white text-slate-900 ' +
        'hover:bg-slate-800 hover:text-white transition-colors';

    return (
        <div className="min-h-screen grid place-items-center p-6">
            <div className="relative w-full max-w-2xl rounded-[28px] border bg-background p-10 shadow-sm">
                <h2 className="text-center text-2xl font-semibold mb-8 text-plate-800">Add new FS</h2>

                <form onSubmit={onSubmit} className="space-y-6">
                    <div>
                        <label className="block text-sm font-medium mb-1 text-plate-800">Name</label>
                        <Input
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            maxLength={60}
                            placeholder="FS name"
                        />
                        <div className="text-xs mt-1 text-slate-500">Min 2, max 40 characters.</div>
                        {errors.name && <div className="text-sm text-red-500 mt-1">{errors.name}</div>}
                    </div>

                    <div>
                        <label className="block text-sm font-medium mb-1 text-plate-800">DB Key</label>
                        <Input
                            value={dbKey}
                            onChange={(e) => setDbKey(e.target.value)}
                            maxLength={60}
                            placeholder="e.g. dark_mode"
                        />
                        <div className="text-xs mt-1 text-slate-500">
                            Lowercase, numbers, dash or underscore (2–40 chars). This is the identifier used in the
                            DB/API.
                        </div>
                        {errors.dbKey && <div className="text-sm text-red-500 mt-1">{errors.dbKey}</div>}
                    </div>

                    <div className="flex gap-3 justify-center pt-2">
                        <a href="/dashboard/feature-switches">
                            <button type="button" className={outlineBtn}>
                                Cancel
                            </button>
                        </a>

                        <button
                            type="submit"
                            className="px-4 py-2 rounded-md bg-teal-500 text-white hover:bg-teal-600 transition-colors"
                            title="Add feature switch"
                        >
                            Add FS
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
