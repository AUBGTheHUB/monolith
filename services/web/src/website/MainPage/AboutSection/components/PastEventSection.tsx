import EventTicket from './EventTicket.tsx';
import pastEvents from '../StaticContent/pastEvents.json';
import SimpleHorizontalCarousel from '@/components/ui/simpleHorizontalCarousel.tsx';

const PastEventSection = () => {
    const eventTickets = pastEvents.map((pastEvent, index) => (
        <EventTicket imgSrc={pastEvent.cover_picture} title={pastEvent.title} tags={pastEvent.tags} key={index} />
    ));
    return (
        <div className="space-y-7 font-mont">
            <h1 className="font-semibold text-3xl text-primary mb-10">Our Past Events</h1>
            <div>
                <SimpleHorizontalCarousel items={eventTickets} itemsPerSlide={1} />
            </div>
        </div>
    );
};

export default PastEventSection;
