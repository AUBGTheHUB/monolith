'use client';
import events from './data/PastEvents.json';
import { PastEventForm } from './components/PastEventForm';
import { useParams } from 'react-router';
import { PastEventFormValues } from './components/schema';

export const EditPastEventPage = () => {
    const { id } = useParams() as { id: string };
    const event = events.find((e) => e.id.toString() === id);

    if (!event)
        return <div className="text-lg min-h-screen text-white flex items-center justify-center">Event not found.</div>;

    const handleUpdate = (data: PastEventFormValues) => {
        console.log('Mock update:', data);
        alert('Event updated (mocked)');
    };

    return (
        <div className="p-8 min-h-screen text-white flex flex-col items-center">
            <h1 className="text-2xl font-semibold mb-6">Edit Past Event</h1>
            <PastEventForm defaultValues={event} onSubmit={handleUpdate} submitLabel="Update Event" />
        </div>
    );
};

export default EditPastEventPage;
