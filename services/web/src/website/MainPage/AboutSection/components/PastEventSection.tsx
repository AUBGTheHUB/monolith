import EventTicket from './EventTicket.tsx';
import pastEvents from '../StaticContent/pastEvents.json';

export default function PastEventSection() {
    return (
        <div className="space-y-7 font-mont" id="past-events">
            <h2 className="font-semibold text-3xl text-primary mb-10">Our Past Events</h2>
            <div className="flex gap-4 flex-wrap w-full justify-center sm:justify-start">
                {pastEvents.map((pastEvent, index) => (
                    <EventTicket
                        imgSrc={pastEvent.cover_picture}
                        title={pastEvent.title}
                        tags={pastEvent.tags}
                        key={index}
                    />
                ))}
            </div>
        </div>
    );
}
