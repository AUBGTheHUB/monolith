import EventTicket from './EventTicket.tsx'
import pastEvents from '../StaticContent/pastEvents.json'

const PastEventSection = () => {
    return (
        <div className="space-y-7 font-mont">
            <h1 className="font-semibold text-3xl text-primary mb-10">Our Past Events</h1>
            <div className="flex flex-row gap-4">
                {pastEvents.map((pastEvent) => (
                    <EventTicket imgSrc={pastEvent.cover_picture} title={pastEvent.title} tags={pastEvent.tags} />
                ))}
            </div>
        </div>
    );
};

export default PastEventSection;
