import { useRef } from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import { Button } from '@/components/ui/button';
import type { WinnerSelection } from '../types';

interface WinnerConfirmationDialogProps {
    selection: WinnerSelection | null;
    isPending: boolean;
    error: Error | null;
    onCancel: () => void;
    onConfirm: () => void;
    onReturnFocus: () => void;
}

export function WinnerConfirmationDialog({
    selection,
    isPending,
    error,
    onCancel,
    onConfirm,
    onReturnFocus,
}: WinnerConfirmationDialogProps) {
    const cancelRef = useRef<HTMLButtonElement>(null);

    return (
        <Dialog.Root
            open={selection !== null}
            onOpenChange={(open) => {
                if (!open && !isPending) onCancel();
            }}
        >
            <Dialog.Portal>
                <Dialog.Overlay className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm" />
                <Dialog.Content
                    className="fixed left-1/2 top-1/2 z-50 max-h-[85dvh] w-[calc(100%_-_2rem)] max-w-lg -translate-x-1/2 -translate-y-1/2 overflow-y-auto rounded-2xl border border-white/20 bg-[#0B1E3B] p-6 text-white shadow-2xl"
                    onOpenAutoFocus={(event) => {
                        event.preventDefault();
                        cancelRef.current?.focus();
                    }}
                    onCloseAutoFocus={(event) => {
                        event.preventDefault();
                        onReturnFocus();
                    }}
                    onEscapeKeyDown={(event) => {
                        if (isPending) event.preventDefault();
                    }}
                    onInteractOutside={(event) => {
                        if (isPending) event.preventDefault();
                    }}
                >
                    <Dialog.Title className="text-2xl font-bold">Declare winner?</Dialog.Title>
                    <Dialog.Description className="mt-3 break-words leading-relaxed text-blue-100/80">
                        Round {selection?.group.round}:{' '}
                        {selection?.group.teams.map((team) => team?.name ?? 'Awaiting team').join(' vs ')}. Declare{' '}
                        {selection?.team.name} the winner of this match?
                    </Dialog.Description>
                    {error && (
                        <p role="alert" className="mt-4 break-words text-sm text-red-200">
                            Could not save the winner. Try again.
                        </p>
                    )}
                    <div className="mt-6 flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
                        <Button
                            ref={cancelRef}
                            type="button"
                            variant="outline"
                            disabled={isPending}
                            onClick={onCancel}
                            className="border-white/20 bg-white/5 text-white hover:bg-white/10 hover:text-white"
                        >
                            Cancel
                        </Button>
                        <Button
                            type="button"
                            disabled={isPending}
                            onClick={onConfirm}
                            className="bg-[#00B2FF] text-white hover:bg-[#0096D6]"
                        >
                            {isPending ? 'Saving winner…' : 'Confirm winner'}
                        </Button>
                    </div>
                </Dialog.Content>
            </Dialog.Portal>
        </Dialog.Root>
    );
}
