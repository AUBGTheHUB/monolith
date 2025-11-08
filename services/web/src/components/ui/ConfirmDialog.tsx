import { useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';

type Props = {
    open: boolean;
    title?: string;
    description?: string;
    confirmText?: string;
    cancelText?: string;
    onConfirm: () => void;
    onClose: () => void; // Cancel / outside click / Esc
};

export default function ConfirmDialog({
    open,
    title = 'Delete this item?',
    description = 'This action cannot be undone.',
    confirmText = 'Delete',
    cancelText = 'Cancel',
    onConfirm,
    onClose,
}: Props) {
    const containerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (!open) return;
        const onKey = (e: KeyboardEvent) => e.key === 'Escape' && onClose();
        document.addEventListener('keydown', onKey);
        // autofocus Cancel
        const el = containerRef.current?.querySelector<HTMLButtonElement>('[data-autofocus]');
        el?.focus();
        return () => document.removeEventListener('keydown', onKey);
    }, [open, onClose]);

    if (!open) return null;

    return createPortal(
        <div
            className="fixed inset-0 z-[100] bg-black/60 backdrop-blur-sm grid place-items-center px-4"
            onClick={onClose}
            aria-modal="true"
            role="dialog"
        >
            <div
                ref={containerRef}
                // Force white card + dark text so copy is always visible
                className="w-full max-w-md rounded-[18px] border bg-white text-slate-900 p-6 shadow-xl"
                onClick={(e) => e.stopPropagation()}
            >
                <h3 className="text-lg font-semibold">{title}</h3>
                <p className="mt-2 text-sm text-slate-600">{description}</p>

                <div className="mt-6 flex justify-end gap-3">
                    <button
                        type="button"
                        data-autofocus
                        className="px-4 py-2 rounded-md border border-slate-300 bg-white text-slate-900 hover:bg-slate-800 hover:text-white transition-colors"
                        onClick={onClose}
                    >
                        {cancelText}
                    </button>
                    <button
                        type="button"
                        className="px-4 py-2 rounded-md bg-red-600 text-white hover:bg-red-700 transition-colors"
                        onClick={() => {
                            onConfirm();
                            onClose();
                        }}
                    >
                        {confirmText}
                    </button>
                </div>
            </div>
        </div>,
        document.body,
    );
}
