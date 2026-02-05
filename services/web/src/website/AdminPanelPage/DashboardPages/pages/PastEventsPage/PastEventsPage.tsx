import { Fragment, useState } from 'react';
import { Link } from 'react-router';
import { PastEvent } from '@/types/past-events.ts';
import { AdminCard } from '@/internalLibrary/AdminCard/adminCard.tsx';
import { Button } from '@/components/ui/button.tsx';
import { Helmet } from 'react-helmet';
import { Styles } from '../../../AdminStyle.ts';
import { PastEventsPageMessages as MESSAGES } from './messages.tsx';
import { MOCK_PAST_EVENTS } from './mockPastEvents.ts';
import { cn } from '@/lib/utils.ts';

export function PastEventsPage() {
    const [events, setEvents] = useState<PastEvent[]>(MOCK_PAST_EVENTS);

    const handleDelete = (id: string) => {
        const event = events.find((e) => e.id === id);
        if (!event) return;

        if (window.confirm(MESSAGES.DELETE_CONFIRM(event.title))) {
            setEvents((prev) => prev.filter((e) => e.id !== id));
        }
    };

    const renderEventActions = (eventId: string) => (
        <div className="flex gap-3 w-full">
            <Link to={`/admin/dashboard/past-events/${eventId}`} className="flex-1">
                <Button
                    variant="outline"
                    className="w-full bg-white/5 border-white/10 text-white hover:bg-white/20 hover:text-white transition-all"
                >
                    {MESSAGES.EDIT_BUTTON}
                </Button>
            </Link>

            <Button
                variant="destructive"
                className="flex-1 shadow-lg shadow-red-500/10 hover:shadow-red-500/20 transition-all"
                onClick={() => handleDelete(eventId)}
            >
                {MESSAGES.DELETE_BUTTON}
            </Button>
        </div>
    );

    return (
        <>
            <Helmet>
                <title>{MESSAGES.PAGE_TITLE}</title>
            </Helmet>

            <div className={cn('min-h-screen p-8', Styles.backgrounds.primaryGradient)}>
                <div className="max-w-7xl mx-auto">
                    {/* Back */}
                    <Link to="/admin/dashboard">
                        <Button variant="ghost" className={cn('mb-6', Styles.glass.ghostButton)}>
                            {MESSAGES.BACK_BUTTON}
                        </Button>
                    </Link>

                    {/* Header */}
                    <div className="flex justify-between items-center mb-12">
                        <div>
                            <h1 className={cn('text-4xl', Styles.text.title)}>{MESSAGES.HEADING}</h1>
                            <p className={Styles.text.subtitle}>{MESSAGES.SUBTITLE}</p>
                        </div>

                        <Link to="/admin/dashboard/past-events/add">
                            <Button
                                size="lg"
                                style={{ backgroundColor: Styles.colors.hubCyan }}
                                className={cn('px-8 py-6 text-lg', Styles.actions.primaryButton)}
                            >
                                {MESSAGES.ADD_BUTTON}
                            </Button>
                        </Link>
                    </div>

                    {/* Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {events.map((event) => (
                            <AdminCard
                                key={event.id}
                                imageUrl={event.image}
                                imageAlt="No Event Image"
                                title={event.title}
                                subtitle={event.tags.join(', ')}
                                linkedinUrl={event.link}
                                actions={renderEventActions(event.id)}
                                className={Styles.glass.card}
                            />
                        ))}
                    </div>
                </div>
            </div>
        </>
    );
}
