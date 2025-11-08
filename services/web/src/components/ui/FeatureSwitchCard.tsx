import { useState } from 'react';
import { Input } from '@/components/ui/input';
import ConfirmDialog from '@/components/ui/ConfirmDialog';

export type FSCardProps = {
    id: string;
    name: string;
    currentState: boolean;
    onRename: (name: string) => void;
    onToggle: () => void;
    onDelete: () => void;
};

export default function FeatureSwitchCard({ id, name, currentState, onRename, onToggle, onDelete }: FSCardProps) {
    const [isRenaming, setIsRenaming] = useState(false);
    const [draft, setDraft] = useState(name);
    const [confirmOpen, setConfirmOpen] = useState(false);

    const valid = draft.trim().length >= 2 && draft.trim().length <= 40;

    const outlineBtn =
        'px-4 py-2 rounded-md border border-slate-300 bg-white text-slate-900 ' +
        'hover:bg-slate-800 hover:text-white transition-colors';

    return (
        <div className="w-[420px] max-w-full rounded-[22px] border p-6 bg-background shadow-sm">
            {!isRenaming ? (
                <>
                    <div className="text-center">
                        <div className="text-lg font-semibold">{name}</div>
                        <div className="mt-1 text-sm text-muted-foreground">{currentState ? 'On' : 'Off'}</div>
                    </div>

                    <div className="mt-5 flex items-center justify-center gap-3">
                        <button type="button" className={outlineBtn} onClick={() => setIsRenaming(true)}>
                            Rename
                        </button>

                        <button type="button" className={outlineBtn} onClick={onToggle}>
                            Toggle
                        </button>

                        <button
                            type="button"
                            className="px-4 py-2 rounded-md bg-red-600 text-white hover:bg-red-700 transition-colors"
                            onClick={() => setConfirmOpen(true)}
                        >
                            Delete
                        </button>
                    </div>

                    <div className="mt-4 text-center">
                        <a
                            className="text-sm underline text-blue-600 hover:text-blue-500"
                            href={`/dashboard/feature-switches/${id}`}
                        >
                            Edit details
                        </a>
                    </div>
                </>
            ) : (
                <>
                    <div className="w-full">
                        <Input
                            value={draft}
                            onChange={(e) => setDraft(e.target.value)}
                            maxLength={60}
                            placeholder="Feature switch name"
                        />
                        <div className="text-xs text-slate-500 mt-1">Min 2, max 40 characters.</div>
                    </div>

                    <div className="mt-4 flex gap-3 justify-center">
                        <button
                            type="button"
                            disabled={!valid}
                            className={`px-4 py-2 rounded-md transition-colors ${
                                valid
                                    ? 'bg-blue-600 text-white hover:bg-blue-700'
                                    : 'bg-blue-600/60 text-white cursor-not-allowed'
                            }`}
                            onClick={() => {
                                onRename(draft.trim());
                                setIsRenaming(false);
                            }}
                        >
                            Save
                        </button>

                        <button
                            type="button"
                            className={outlineBtn}
                            onClick={() => {
                                setDraft(name);
                                setIsRenaming(false);
                            }}
                        >
                            Cancel
                        </button>
                    </div>
                </>
            )}

            {/* Delete confirmation modal */}
            <ConfirmDialog
                open={confirmOpen}
                title="Delete this feature switch?"
                description="This action cannot be undone."
                confirmText="Delete"
                cancelText="Cancel"
                onConfirm={onDelete}
                onClose={() => setConfirmOpen(false)}
            />
        </div>
    );
}
