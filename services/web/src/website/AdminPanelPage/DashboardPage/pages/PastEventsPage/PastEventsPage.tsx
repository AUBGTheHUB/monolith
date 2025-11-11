import events from './data/PastEvents.json';
import { PastEventCard } from './components/PastEventsCard';
import { Button } from '@/components/ui/button';

export const PastEventsPage = () => {
    return (
        <div className="p-8 space-y-6 min-h-screen text-white">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-semibold">Past Events</h1>
                <a href="/dashboard/past-events/add">
                    <Button className="border border-white">Add Event</Button>
                </a>
            </div>

            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                {events.map((e) => (
                    <PastEventCard key={e.id} {...e} />
                ))}
            </div>
        </div>
    );
};

export default PastEventsPage;
