import EventTicket from './EventTicket.tsx';
import pastEvents from '../StaticContent/pastEvents.json';
import '@/components/EmblaCarousel/css/base.css';
import '@/components/EmblaCarousel/css/embla.css';
import EmblaCarousel from '@/components/EmblaCarousel/js/EmblaCarousel.tsx';
import { EmblaOptionsType } from 'embla-carousel';

const PastEventSection = () => {
    const SLIDES = pastEvents.map((pastEvent, index) => (
        <EventTicket imgSrc={pastEvent.cover_picture} title={pastEvent.title} tags={pastEvent.tags} key={index} />
    ));

    const OPTIONS: EmblaOptionsType = { align: 'start', slidesToScroll: 'auto' };

    return (
        <div className="space-y-7 font-mont">
            <h1 className="font-semibold text-3xl text-primary mb-10">Our Past Events</h1>
            <EmblaCarousel slides={SLIDES} options={OPTIONS} />
        </div>
    );
};

export default PastEventSection;
