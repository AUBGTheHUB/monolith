import { useEffect, useState, useRef } from 'react';
import EventTicket from './EventTicket.tsx';
import EventModal from './PastEventSectionModal.tsx';
import { apiClient } from '../../../../services/apiClient.ts';
import { ChevronLeft, ChevronRight, Loader2 } from 'lucide-react';

type EventSummary = {
    id: number;
    title: string;
    cover_picture: string;
    tags: string[];
};

export default function PastEventSection() {
    const [events, setEvents] = useState<EventSummary[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedEventId, setSelectedEventId] = useState<number | null>(null);
    const scrollContainerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const fetchEvents = async () => {
            try {
                const data = await apiClient.get<EventSummary[]>('/api/v3/admin/events');
                setEvents(data);
            } catch (error) {
                console.error(error);
            } finally {
                setLoading(false);
            }
        };

        fetchEvents();
    }, []);

    const scroll = (direction: 'left' | 'right') => {
        if (scrollContainerRef.current) {
            const { current } = scrollContainerRef;
            const scrollAmount = 320;
            if (direction === 'left') {
                current.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
            } else {
                current.scrollBy({ left: scrollAmount, behavior: 'smooth' });
            }
        }
    };

    return (
        <div className="space-y-7 font-mont relative" id="past-events">
            <div className="flex justify-between items-center mb-6">
                <h2 className="font-semibold text-3xl text-primary">Our Past Events</h2>

                <div className="hidden sm:flex gap-2">
                    <button
                        onClick={() => scroll('left')}
                        className="p-2 rounded-full border border-gray-300 hover:bg-gray-100 hover:text-primary transition-colors"
                    >
                        <ChevronLeft className="w-5 h-5" />
                    </button>
                    <button
                        onClick={() => scroll('right')}
                        className="p-2 rounded-full border border-gray-300 hover:bg-gray-100 hover:text-primary transition-colors"
                    >
                        <ChevronRight className="w-5 h-5" />
                    </button>
                </div>
            </div>

            {loading ? (
                <div className="w-full h-60 flex items-center justify-center">
                    <Loader2 className="w-8 h-8 animate-spin text-gray-400" />
                </div>
            ) : events.length > 0 ? (
                <div
                    ref={scrollContainerRef}
                    className="flex gap-6 overflow-x-auto pb-6 snap-x snap-mandatory scrollbar-hide px-1"
                    style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
                >
                    {events.map((event) => (
                        <div key={event.id} className="snap-start shrink-0">
                            <EventTicket
                                imgSrc={event.cover_picture}
                                title={event.title}
                                tags={event.tags}
                                onClick={() => setSelectedEventId(event.id)}
                            />
                        </div>
                    ))}
                </div>
            ) : (
                <p className="text-gray-500">No past events found.</p>
            )}

            {selectedEventId && <EventModal eventId={selectedEventId} onClose={() => setSelectedEventId(null)} />}
        </div>
    );
}
