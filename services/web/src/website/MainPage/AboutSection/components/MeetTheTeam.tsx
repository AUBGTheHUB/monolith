import HubberModule from './HubberModule';
import hubbers from '../StaticContent/hubbers.json';
import '@/components/EmblaCarousel/SlidesPerViewCarousel/css/base.css';
import '@/components/EmblaCarousel/SlidesPerViewCarousel/css/embla-team.css';
import EmblaCarousel from '@/components/EmblaCarousel/SlidesPerViewCarousel/js/EmblaCarousel.tsx';
import { EmblaOptionsType } from 'embla-carousel';
import React from 'react';

const initialSlides: React.ReactElement[] = hubbers.map((hubber, index) => (
    <HubberModule imgSrc={hubber.picture} name={hubber.name} key={index} />
));

const SLIDES: React.ReactElement[][] = chunkArray(initialSlides,2);


function chunkArray(array: React.ReactElement[], chunkSize: number): React.ReactElement[][] {
    return array.reduce((resultArray, item, index) => {
        const chunkIndex = Math.floor(index / chunkSize);
        if (!resultArray[chunkIndex]) {
            resultArray[chunkIndex] = []; // Start a new chunk
        }
        resultArray[chunkIndex].push(item);
        return resultArray;
    }, [] as React.ReactElement[][]);
}

const OPTIONS: EmblaOptionsType = { align: 'start', slidesToScroll: 'auto', loop:true,watchSlides:true };

export default function PastEventSection() {
    return (
        <div className="space-y-7 font-mont">
            <h2 className="font-semibold text-3xl text-primary mb-10">Meet the team</h2>
            <EmblaCarousel type="team" slides={SLIDES} options={OPTIONS} />
        </div>
    );
}
