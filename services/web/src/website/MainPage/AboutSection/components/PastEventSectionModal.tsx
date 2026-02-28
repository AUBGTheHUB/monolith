import { useEffect } from 'react';
import { apiClient } from '@/services/apiClient.ts';
import { Button } from '@/components/ui/button';
import { X, Loader2 } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import { PastEvent } from '@/types/past-events.ts';

type EventModalProps = {
    eventId: string;
    onClose: () => void;
};

export default function EventModal({ eventId, onClose }: EventModalProps) {
    const { isLoading, data: event } = useQuery({
        queryKey: ['event'],
        queryFn: () => apiClient.get<{ past_event: PastEvent }>(`/admin/events/${eventId}`),
        select: (res) => res.past_event,
    });

    useEffect(() => {
        const handleEsc = (e: KeyboardEvent) => {
            if (e.key === 'Escape') onClose();
        };
        window.addEventListener('keydown', handleEsc);
        return () => window.removeEventListener('keydown', handleEsc);
    }, [onClose]);

    if (!eventId) return null;

    return (
        <div
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-in fade-in duration-200"
            onClick={onClose}
        >
            <div
                className="relative w-full max-w-3xl max-h-[90vh] overflow-y-auto bg-white rounded-2xl shadow-2xl flex flex-col"
                onClick={(e) => e.stopPropagation()}
            >
                <button
                    onClick={onClose}
                    className="absolute right-4 top-4 p-2 bg-white/80 rounded-full hover:bg-gray-100 transition-colors z-10"
                >
                    <X className="w-6 h-6 text-gray-800" />
                </button>

                {isLoading ? (
                    <div className="flex h-64 items-center justify-center">
                        <Loader2 className="w-8 h-8 animate-spin text-primary" />
                    </div>
                ) : event ? (
                    <>
                        <div className="w-full h-64 sm:h-80 relative shrink-0">
                            <img src={event.cover_picture} alt={event.title} className="w-full h-full object-cover" />
                            <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                            <h2 className="absolute bottom-6 left-6 text-3xl font-bold text-white drop-shadow-md">
                                {event.title}
                            </h2>
                        </div>

                        <div className="flex flex-wrap gap-2">
                            {event.tags.map((tag, idx) => (
                                <Button key={idx} variant="tag_xs" size="round_xs">
                                    {tag.toUpperCase()}
                                </Button>
                            ))}
                        </div>

                        <div className="prose max-w-none text-gray-700 leading-relaxed">
                            <p>{event.description || 'No description available.'}</p>
                        </div>
                    </>
                ) : null}
            </div>
        </div>
    );
}
