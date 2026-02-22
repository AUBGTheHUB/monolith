import { useEffect, useState } from 'react';
import { apiClient } from '../../../../services/apiClient.ts';
import { Button } from '@/components/ui/button';
import { X, Calendar, MapPin, Loader2 } from 'lucide-react';

type EventDetail = {
    id: number;
    title: string;
    description: string;
    location?: string;
    date?: string;
    tags: string[];
    cover_picture: string;
};

type EventModalProps = {
    eventId: number;
    onClose: () => void;
};

export default function EventModal({ eventId, onClose }: EventModalProps) {
    const [event, setEvent] = useState<EventDetail | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchDetails = async () => {
            try {
                setLoading(true);
                const data = await apiClient.get<EventDetail>(`/api/v3/admin/events/${eventId}`);
                setEvent(data);
            } catch (err) {
                console.error(err);
                setError('Failed to load event details.');
            } finally {
                setLoading(false);
            }
        };

        if (eventId) {
            fetchDetails();
        }
    }, [eventId]);

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

                {loading ? (
                    <div className="flex h-64 items-center justify-center">
                        <Loader2 className="w-8 h-8 animate-spin text-primary" />
                    </div>
                ) : error ? (
                    <div className="flex h-64 items-center justify-center text-red-500">{error}</div>
                ) : event ? (
                    <>
                        <div className="w-full h-64 sm:h-80 relative shrink-0">
                            <img src={event.cover_picture} alt={event.title} className="w-full h-full object-cover" />
                            <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                            <h2 className="absolute bottom-6 left-6 text-3xl font-bold text-white drop-shadow-md">
                                {event.title}
                            </h2>
                        </div>

                        <div className="p-6 sm:p-8 space-y-6">
                            <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                                {event.date && (
                                    <div className="flex items-center gap-2">
                                        <Calendar className="w-4 h-4 text-primary" />
                                        <span>{new Date(event.date).toLocaleDateString()}</span>
                                    </div>
                                )}
                                {event.location && (
                                    <div className="flex items-center gap-2">
                                        <MapPin className="w-4 h-4 text-primary" />
                                        <span>{event.location}</span>
                                    </div>
                                )}
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
                        </div>
                    </>
                ) : null}
            </div>
        </div>
    );
}
