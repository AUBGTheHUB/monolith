import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

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
    const valid = draft.trim().length >= 2 && draft.trim().length <= 40;

    return (
        <div className="rounded-2xl border p-4 flex flex-col items-center gap-3">
            {!isRenaming ? (
                <>
                    <div className="text-lg font-semibold text-center">{name}</div>
                    <div className="text-sm text-gray-500">{currentState ? 'On' : 'Off'}</div>

                    <div className="flex gap-2">
                        <Button variant="outline" onClick={() => setIsRenaming(true)}>
                            Rename
                        </Button>
                        <Button variant="outline" onClick={onToggle}>
                            Toggle
                        </Button>
                        <Button
                            variant="destructive"
                            onClick={() => {
                                if (confirm('Delete this feature switch?')) onDelete();
                            }}
                        >
                            Delete
                        </Button>
                    </div>

                    <a className="text-sm underline text-blue-600" href={`/dashboard/feature-switches/${id}`}>
                        Edit details
                    </a>
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
                        <div className="text-xs text-gray-500 mt-1">Min 2, max 40 characters.</div>
                    </div>
                    <div className="flex gap-2">
                        <Button
                            disabled={!valid}
                            onClick={() => {
                                onRename(draft.trim());
                                setIsRenaming(false);
                            }}
                        >
                            Save
                        </Button>
                        <Button
                            variant="outline"
                            onClick={() => {
                                setDraft(name);
                                setIsRenaming(false);
                            }}
                        >
                            Cancel
                        </Button>
                    </div>
                </>
            )}
        </div>
    );
}
