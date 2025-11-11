'use client';
import { PastEventForm, PastEventFormProps } from './components/PastEventForm';

export const AddPastEventPage = () => {
    const handleCreate = (data: PastEventFormProps) => {
        console.log('Mock create:', data);
        alert('Event created (mocked)');
    };

    return (
        <div className="p-8 min-h-screen text-white flex flex-col items-center">
            <h1 className="text-2xl font-semibold mb-6">Edit Past Event</h1>
            <PastEventForm onSubmit={handleCreate} submitLabel="Create Event" />
        </div>
    );
};

export default AddPastEventPage;
