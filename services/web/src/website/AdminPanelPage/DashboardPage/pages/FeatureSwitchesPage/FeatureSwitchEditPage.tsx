import { useEffect, useMemo, useState } from 'react';
import { Input } from '@/components/ui/input';
import ConfirmDialog from '@/components/ui/ConfirmDialog';
import {
    getFeatureSwitchById,
    updateFeatureSwitch,
    deleteFeatureSwitch,
    type FeatureSwitch,
} from '@/website/AdminPanelPage/DashboardPage/pages/FeatureSwitchesPage/store/useFeatureSwitches';

// Read :id from the URL path, e.g. /dashboard/feature-switches/<id>
function useIdFromPath(): string | null {
    const p = typeof window !== 'undefined' ? window.location.pathname : '';
    const parts = p.split('/');
    const last = parts[parts.length - 1];
    return last || null;
}

export default function FeatureSwitchEditPage() {
    const id = useIdFromPath();
    const existing = useMemo<FeatureSwitch | undefined>(() => (id ? getFeatureSwitchById(id) : undefined), [id]);

    const [notFound, setNotFound] = useState<boolean>(false);

    // Form state
    const [name, setName] = useState<string>(existing?.name ?? '');
    const [dbKey, setDbKey] = useState<string>(existing?.dbKey ?? existing?.id ?? '');
    const [errors, setErrors] = useState<{ name?: string }>({});

    // Delete confirm dialog
    const [confirmOpen, setConfirmOpen] = useState<boolean>(false);

    useEffect(() => {
        if (!id || !existing) {
            setNotFound(true);
        } else {
            setNotFound(false);
            setName(existing.name);
            setDbKey(existing.dbKey ?? existing.id);
        }
    }, [id, existing]);

    if (!id || notFound) {
        return (
            <div className="min-h-screen grid place-items-center p-6">
                <div className="w-full max-w-2xl rounded-[28px] border bg-white p-10 shadow-sm text-center">
                    <h2 className="text-2xl font-semibold mb-6 text-slate-900">Feature not found</h2>
                    <a
                        href="/dashboard/feature-switches"
                        className="inline-block px-4 py-2 rounded-md border border-slate-300 bg-white text-slate-900 hover:bg-slate-800 hover:text-white transition-colors"
                    >
                        Back to list
                    </a>
                </div>
            </div>
        );
    }

    const fsId: string = id; // narrowed after the guard

    function validate(): boolean {
        const e: { name?: string } = {};
        const n = name.trim();
        if (n.length < 2 || n.length > 40) e.name = 'Name must be 2–40 characters.';
        setErrors(e);
        return Object.keys(e).length === 0;
    }

    function onSubmit(e: React.FormEvent) {
        e.preventDefault();
        if (!validate()) return;

        updateFeatureSwitch(fsId, { name: name.trim() });
        window.location.assign('/dashboard/feature-switches');
    }

    function onDeleteConfirm() {
        deleteFeatureSwitch(fsId);
        window.location.assign('/dashboard/feature-switches');
    }

    const outlineBtn =
        'px-4 py-2 rounded-md border border-slate-300 bg-white text-slate-900 ' +
        'hover:bg-slate-800 hover:text-white transition-colors';

    return (
        <div className="min-h-screen grid place-items-center p-6">
            {/* Explicit white card so all dark text is readable */}
            <div className="relative w-full max-w-2xl rounded-[28px] border bg-white p-10 shadow-sm">
                <h2 className="text-center text-2xl font-semibold mb-8 text-slate-900">Edit feature switch</h2>

                <form onSubmit={onSubmit} className="space-y-6">
                    {/* Name */}
                    <div>
                        <label className="block text-sm font-medium mb-1 text-slate-900">Name</label>
                        <Input
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            maxLength={60}
                            placeholder="FS name"
                        />
                        <div className="text-xs mt-1 text-slate-600">Min 2, max 40 characters.</div>
                        {errors.name && <div className="text-sm text-red-600 mt-1">{errors.name}</div>}
                    </div>

                    {/* DB Key (read-only for now) */}
                    <div>
                        <label className="block text-sm font-medium mb-1 text-slate-900">DB Key</label>
                        <Input
                            value={dbKey}
                            disabled
                            readOnly
                            className="bg-slate-100 text-slate-700"
                            placeholder="e.g. dark_mode"
                        />
                        <div className="text-xs mt-1 text-slate-600">
                            Identifier used in DB/API. (Locked here to avoid breaking references.)
                        </div>
                    </div>

                    {/* Actions */}
                    <div className="flex gap-3 justify-center pt-2">
                        <a href="/dashboard/feature-switches">
                            <button type="button" className={outlineBtn}>
                                Cancel
                            </button>
                        </a>
                        <button
                            type="submit"
                            className="px-4 py-2 rounded-md bg-blue-600 text-white hover:bg-blue-700 transition-colors"
                        >
                            Save changes
                        </button>
                    </div>
                </form>

                {/* Delete section */}
                <div className="mt-8 flex justify-center">
                    <button
                        type="button"
                        className="px-4 py-2 rounded-md bg-red-600 text-white hover:bg-red-700 transition-colors"
                        onClick={() => setConfirmOpen(true)}
                    >
                        Delete
                    </button>
                </div>
            </div>

            {/* Confirm delete dialog */}
            <ConfirmDialog
                open={confirmOpen}
                title="Delete this feature switch?"
                description="This action cannot be undone."
                confirmText="Delete"
                cancelText="Cancel"
                onConfirm={onDeleteConfirm}
                onClose={() => setConfirmOpen(false)}
            />
        </div>
    );
}
