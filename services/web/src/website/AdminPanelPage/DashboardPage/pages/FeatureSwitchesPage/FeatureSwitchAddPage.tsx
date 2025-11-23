import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { featureSwitchSchema, type FeatureSwitchForm } from './schema';
import { createFeatureSwitch } from '@/website/AdminPanelPage/DashboardPage/pages/FeatureSwitchesPage/store/useFeatureSwitches';
import { Input } from '@/components/ui/input';

export default function FeatureSwitchAddPage() {
    const form = useForm<FeatureSwitchForm>({
        resolver: zodResolver(featureSwitchSchema),
        defaultValues: { name: '' },
    });

    const outlineBtn =
        'px-4 py-2 rounded-md border border-slate-300 bg-white text-slate-900 ' +
        'hover:bg-slate-800 hover:text-white transition-colors';

    const onSubmit = (data: FeatureSwitchForm) => {
        createFeatureSwitch({ name: data.name.trim(), currentState: false }); // default Off
        window.location.assign('/dashboard/feature-switches');
    };

    const nameError = form.formState.errors.name?.message;

    return (
        <div className="min-h-screen grid place-items-center p-6">
            <div className="relative w-full max-w-2xl rounded-[28px] border bg-white p-10 shadow-sm">
                <h2 className="text-center text-2xl font-semibold mb-8 text-slate-900">Add new FS</h2>

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
