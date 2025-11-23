import { useEffect, useMemo, useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Input } from '@/components/ui/input';
import ConfirmDialog from '@/components/ui/ConfirmDialog';
import { featureSwitchSchema, type FeatureSwitchForm } from './schema';
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
    const [confirmOpen, setConfirmOpen] = useState<boolean>(false);

    useEffect(() => {
        setNotFound(!id || !existing);
    }, [id, existing]);

    const form = useForm<FeatureSwitchForm>({
        resolver: zodResolver(featureSwitchSchema),
        defaultValues: { name: existing?.name ?? '' },
    });

    useEffect(() => {
        if (existing) form.reset({ name: existing.name });
    }, [existing, form]);

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

    const fsId: string = id;

    const outlineBtn =
        'px-4 py-2 rounded-md border border-slate-300 bg-white text-slate-900 ' +
        'hover:bg-slate-800 hover:text-white transition-colors';

    const nameError = form.formState.errors.name?.message;

    const onSubmit = (data: FeatureSwitchForm) => {
        updateFeatureSwitch(fsId, { name: data.name.trim() });
        window.location.assign('/dashboard/feature-switches');
    };

    function onDeleteConfirm() {
        deleteFeatureSwitch(fsId);
        window.location.assign('/dashboard/feature-switches');
    }

    return (
        <div className="min-h-screen grid place-items-center p-6">
            <div className="relative w-full max-w-2xl rounded-[28px] border bg-white p-10 shadow-sm">
                <h2 className="text-center text-2xl font-semibold mb-8 text-slate-900">Edit feature switch</h2>

                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                    <div>
                        <label className="block text-sm font-medium mb-1 text-slate-900">Name</label>
                        <Input placeholder="FS name" maxLength={12} {...form.register('name')} />
                        <div className="text-xs mt-1 text-slate-600">Min 2, max 12 characters.</div>
                        {nameError && <div className="text-sm text-red-600 mt-1">{nameError}</div>}
                    </div>

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
