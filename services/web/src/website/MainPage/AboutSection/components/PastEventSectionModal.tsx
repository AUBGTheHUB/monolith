import { useEffect } from 'react';
import { createPortal } from 'react-dom';
import { apiClient } from '@/services/apiClient.ts';
import { Button } from '@/components/ui/button';
import { X, Loader2 } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import { PastEvent } from '@/types/past-events.ts';

type EventModalProps = {
    event: PastEvent;
    onClose: () => void;
};

export default function EventModal({ event: fallbackEvent, onClose }: EventModalProps) {
    const { isLoading, data: fetchedEvent } = useQuery({
        queryKey: ['event', fallbackEvent.id],
        queryFn: () => apiClient.get<{ past_event: PastEvent }>(`/admin/events/${fallbackEvent.id}`),
        select: (res) => res.past_event,
        retry: false,
    });

    const event = fetchedEvent ?? fallbackEvent;

    useEffect(() => {
        const handleEsc = (e: KeyboardEvent) => {
            if (e.key === 'Escape') onClose();
        };
        window.addEventListener('keydown', handleEsc);
        document.body.style.overflow = 'hidden';
        return () => {
            window.removeEventListener('keydown', handleEsc);
            document.body.style.overflow = '';
        };
    }, [onClose]);

    return createPortal(
        <div
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-in fade-in duration-200"
            onClick={onClose}
        >
            <div
                className="relative flex w-full max-w-4xl max-h-[90vh] flex-col overflow-hidden rounded-3xl bg-white shadow-2xl"
                onClick={(e) => e.stopPropagation()}
            >
                <button
                    onClick={onClose}
                    className="absolute right-4 top-4 z-20 rounded-full bg-white/90 p-2 shadow-sm transition-colors hover:bg-gray-100"
                >
                    <X className="w-6 h-6 text-gray-800" />
                </button>

                {isLoading && !fetchedEvent ? (
                    <div className="flex h-64 items-center justify-center">
                        <Loader2 className="w-8 h-8 animate-spin text-primary" />
                    </div>
                ) : event ? (
                    <>
                        <div className="relative w-full aspect-[16/9] max-h-[26rem] shrink-0 overflow-hidden bg-gray-100">
                            <img
                                src={event.cover_picture}
                                alt=""
                                aria-hidden
                                className="absolute inset-0 h-full w-full scale-110 object-cover blur-2xl opacity-40"
                            />
                            <div className="absolute inset-0 bg-gradient-to-t from-black/45 via-black/10 to-transparent" />
                            <img
                                src={event.cover_picture}
                                alt={event.title}
                                className="relative z-10 h-full w-full object-contain p-4 sm:p-6"
                            />
                            <h2 className="absolute bottom-5 left-5 right-16 z-20 text-2xl font-bold leading-tight text-white drop-shadow-md sm:text-3xl">
                                {event.title}
                            </h2>
                        </div>

                        <div className="space-y-5 overflow-y-auto px-5 py-5 sm:px-8 sm:py-6">
                            {event.tags.length > 0 ? (
                                <div className="flex flex-wrap gap-2">
                                    {event.tags.map((tag, idx) => (
                                        <Button key={idx} variant="tag_xs" size="round_xs">
                                            {tag.toUpperCase()}
                                        </Button>
                                    ))}
                                </div>
                            ) : null}

                            <div className="rounded-2xl border bg-gray-50/70 p-4 sm:p-5">
                                <h3 className="mb-2 text-lg font-semibold text-primary">About this event</h3>
                                <div className="prose max-w-none text-gray-700 leading-relaxed">
                                    <p>{event.description || 'No description available.'}</p>
                                </div>
                            </div>
                        </div>
                    </>
                ) : null}
            </div>
        </div>,
        document.body,
    );
}
