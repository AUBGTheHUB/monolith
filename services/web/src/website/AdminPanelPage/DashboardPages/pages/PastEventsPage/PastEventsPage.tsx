import { useState, useRef } from 'react';
import { Link } from 'react-router';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Helmet } from 'react-helmet';
import { ChevronLeft, ChevronRight, Edit, Trash2, X, Tag, Image as ImageIcon } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import { Styles } from '../../../AdminStyle';
import { apiClient } from '@/services/apiClient';
import { PastEvent } from '@/types/past-events';
import { PastEventsPageMessages as MESSAGES } from './messages';

export function PastEventsPage() {
    const queryClient = useQueryClient();
    const [selectedEventId, setSelectedEventId] = useState<string | null>(null);
    const scrollContainerRef = useRef<HTMLDivElement>(null);

    // Fetch All Events
    const { data: events, isLoading: isListLoading } = useQuery({
        queryKey: ['events'],
        queryFn: () => apiClient.get<{ past_events: PastEvent[] }>('/admin/events'),
        select: (res) => res.past_events,
    });

    // Fetch Single Event Details
    const { data: selectedEvent, isLoading: isDetailLoading } = useQuery({
        queryKey: ['event', selectedEventId],
        queryFn: () => apiClient.get<{ past_event: PastEvent }>(`/admin/events/${selectedEventId}`),
        select: (res) => res.past_event,
        enabled: !!selectedEventId,
    });

    // Delete Mutation
    const deleteMutation = useMutation({
        mutationFn: (id: string) => apiClient.delete(`/admin/events/${id}`),
        onSuccess: async () => {
            await queryClient.invalidateQueries({ queryKey: ['events'] });
            setSelectedEventId(null);
        },
        onError: (error) => alert(error.message),
    });

    // Handlers
    const scroll = (direction: 'left' | 'right') => {
        if (scrollContainerRef.current) {
            const container = scrollContainerRef.current;
            const scrollAmount = 400;
            const targetScroll =
                direction === 'left' ? container.scrollLeft - scrollAmount : container.scrollLeft + scrollAmount;

            container.scrollTo({
                left: targetScroll,
                behavior: 'smooth',
            });
        }
    };

    const handleDelete = () => {
        if (selectedEvent && window.confirm(MESSAGES.DELETE_CONFIRM(selectedEvent.title))) {
            deleteMutation.mutate(selectedEvent.id);
        }
    };

    // Render Helpers
    const pageWrapperClass = cn('min-h-screen p-8', Styles.backgrounds.primaryGradient);

    if (isListLoading) {
        return (
            <div className={pageWrapperClass}>
                <div className="max-w-7xl mx-auto text-white text-center py-20 animate-pulse">
                    {MESSAGES.LOADING_STATE}
                </div>
            </div>
        );
    }

    return (
        <>
            <Helmet>
                <title>{MESSAGES.PAGE_TITLE}</title>
            </Helmet>

            <div className={pageWrapperClass}>
                <div className="max-w-7xl mx-auto flex flex-col h-full">
                    {/* Header */}
                    <div className="flex justify-between items-start mb-8">
                        <div>
                            <Link to="/admin/dashboard">
                                <Button
                                    variant="ghost"
                                    className={cn('mb-4 pl-0 hover:bg-transparent', Styles.glass.ghostButton)}
                                >
                                    {MESSAGES.BACK_BUTTON}
                                </Button>
                            </Link>
                            <h1 className={cn('text-4xl', Styles.text.title)}>{MESSAGES.HEADING}</h1>
                            <p className={Styles.text.subtitle}>{MESSAGES.SUBTITLE}</p>
                        </div>

                        <Link to="/admin/dashboard/past-events/add">
                            <Button
                                size="lg"
                                style={{ backgroundColor: Styles.colors.hubCyan }}
                                className={cn(
                                    'px-6 py-6 text-lg shadow-lg shadow-cyan-500/20',
                                    Styles.actions.primaryButton,
                                )}
                            >
                                {MESSAGES.ADD_BUTTON}
                            </Button>
                        </Link>
                    </div>

                    {!events || events.length === 0 ? (
                        <Card className={cn('p-20 text-center border-dashed', Styles.glass.card)}>
                            <p className={cn('text-xl font-medium', Styles.text.subtitle)}>{MESSAGES.EMPTY_STATE}</p>
                        </Card>
                    ) : (
                        /* Carousel*/
                        <div className="relative group mt-10">
                            {/* Left Arrow */}
                            <button
                                onClick={() => scroll('left')}
                                className="absolute left-0 top-1/2 -translate-y-1/2 -translate-x-4 z-10 p-3 rounded-full bg-black/50 hover:bg-black/80 text-white backdrop-blur-sm transition-all opacity-0 group-hover:opacity-100 disabled:opacity-0"
                            >
                                <ChevronLeft size={24} />
                            </button>

                            {/* Scroll Container */}
                            <div
                                ref={scrollContainerRef}
                                className="flex gap-6 overflow-x-auto pb-10 px-2 snap-x snap-mandatory scrollbar-hide"
                                style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
                            >
                                {events.map((event) => (
                                    <div
                                        key={event.id}
                                        onClick={() => setSelectedEventId(event.id)}
                                        className="min-w-[300px] md:min-w-[350px] snap-center cursor-pointer transform transition-all duration-300 hover:scale-[1.02]"
                                    >
                                        <Card
                                            className={cn(
                                                'h-full overflow-hidden border-0 relative group/card',
                                                Styles.glass.card,
                                            )}
                                        >
                                            {/* Image Area */}
                                            <div className="relative h-48 w-full overflow-hidden bg-gray-900">
                                                <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent z-10" />
                                                {event.cover_picture ? (
                                                    <img
                                                        src={event.cover_picture}
                                                        alt={event.title}
                                                        className="w-full h-full object-cover transition-transform duration-500 group-hover/card:scale-110"
                                                        onError={(e) => {
                                                            (e.target as HTMLImageElement).src =
                                                                'https://placehold.co/600x400?text=No+Image';
                                                        }}
                                                    />
                                                ) : (
                                                    <div className="w-full h-full flex items-center justify-center text-gray-500">
                                                        <ImageIcon size={40} />
                                                    </div>
                                                )}
                                            </div>

                                            {/* Content Area */}
                                            <div className="p-5">
                                                <h3 className="text-xl font-bold text-white mb-3 line-clamp-1">
                                                    {event.title}
                                                </h3>

                                                <div className="flex flex-wrap gap-2">
                                                    {event.tags && event.tags.length > 0 ? (
                                                        <>
                                                            {event.tags.slice(0, 3).map((tag) => (
                                                                <Badge
                                                                    key={tag}
                                                                    variant="secondary"
                                                                    className="bg-white/10 text-white hover:bg-white/20 border-0 text-xs"
                                                                >
                                                                    {tag}
                                                                </Badge>
                                                            ))}
                                                            {event.tags.length > 3 && (
                                                                <span className="text-xs text-gray-400 self-center">
                                                                    +{event.tags.length - 3}
                                                                </span>
                                                            )}
                                                        </>
                                                    ) : (
                                                        <span className="text-xs text-gray-500 italic">No tags</span>
                                                    )}
                                                </div>
                                            </div>
                                        </Card>
                                    </div>
                                ))}
                            </div>

                            {/* Right Arrow */}
                            <button
                                onClick={() => scroll('right')}
                                className="absolute right-0 top-1/2 -translate-y-1/2 translate-x-4 z-10 p-3 rounded-full bg-black/50 hover:bg-black/80 text-white backdrop-blur-sm transition-all opacity-0 group-hover:opacity-100"
                            >
                                <ChevronRight size={24} />
                            </button>
                        </div>
                    )}

                    {/* Event Details */}
                    {selectedEventId && (
                        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
                            {/* Backdrop */}
                            <div
                                className="absolute inset-0 bg-black/80 backdrop-blur-sm transition-opacity"
                                onClick={() => setSelectedEventId(null)}
                            />

                            {/* Modal Content */}
                            <div
                                className={cn(
                                    'relative w-full max-w-4xl max-h-[90vh] overflow-y-auto rounded-2xl shadow-2xl border border-white/10 animate-in fade-in zoom-in duration-200',
                                    Styles.backgrounds.primaryGradient,
                                )}
                            >
                                <button
                                    onClick={() => setSelectedEventId(null)}
                                    className="absolute top-4 right-4 z-50 p-2 bg-black/50 hover:bg-white/20 rounded-full text-white transition-colors"
                                >
                                    <X size={20} />
                                </button>

                                {isDetailLoading || !selectedEvent ? (
                                    <div className="p-20 text-center text-white">Loading details...</div>
                                ) : (
                                    <div className="grid md:grid-cols-2">
                                        {/* Left: Image */}
                                        <div className="relative h-64 md:h-auto min-h-[300px] bg-black">
                                            {selectedEvent.cover_picture ? (
                                                <img
                                                    src={selectedEvent.cover_picture}
                                                    alt={selectedEvent.title}
                                                    className="w-full h-full object-cover absolute inset-0"
                                                />
                                            ) : (
                                                <div className="absolute inset-0 flex items-center justify-center text-gray-500">
                                                    <ImageIcon size={60} />
                                                </div>
                                            )}
                                            <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-transparent to-transparent md:bg-gradient-to-r" />
                                        </div>

                                        {/* Right: Content */}
                                        <div className="p-8 flex flex-col h-full bg-[#0a0a0a]/50 backdrop-blur-xl">
                                            <div className="flex-1">
                                                <h2 className="text-3xl font-bold text-white mb-6">
                                                    {selectedEvent.title}
                                                </h2>

                                                <div className="flex flex-wrap gap-2 mb-6">
                                                    {selectedEvent.tags?.map((tag) => (
                                                        <Badge
                                                            key={tag}
                                                            className="bg-white/10 text-white border-white/20 px-3 py-1 text-sm"
                                                        >
                                                            <Tag size={14} className="mr-2" /> {tag}
                                                        </Badge>
                                                    ))}
                                                </div>
                                            </div>

                                            {/* Action Buttons */}
                                            <div className="mt-8 pt-6 border-t border-white/10 flex gap-4">
                                                <Link
                                                    to={`/admin/dashboard/past-events/${selectedEvent.id}`}
                                                    className="flex-1"
                                                >
                                                    <Button className="w-full bg-white text-black hover:bg-gray-200 font-semibold gap-2">
                                                        <Edit size={16} /> Edit Event
                                                    </Button>
                                                </Link>
                                                <Button
                                                    variant="destructive"
                                                    className="flex-1 gap-2 bg-red-500/10 text-red-400 border border-red-500/50 hover:bg-red-500 hover:text-white"
                                                    onClick={handleDelete}
                                                    disabled={deleteMutation.isPending}
                                                >
                                                    <Trash2 size={16} />
                                                    {deleteMutation.isPending ? 'Deleting...' : 'Delete'}
                                                </Button>
                                            </div>
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </>
    );
}
