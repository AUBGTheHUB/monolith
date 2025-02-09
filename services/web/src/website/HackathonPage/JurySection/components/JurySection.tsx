import JuryModule from '../../JurySection/components/JuryModule';
import jury from '../StaticContent/jury.json';
import '@/components/EmblaCarousel/SlidesPerViewCarousel/css/base.css';
import '@/components/EmblaCarousel/SlidesPerViewCarousel/css/embla-jury.css';
import EmblaCarousel from '@/components/EmblaCarousel/SlidesPerViewCarousel/js/EmblaCarousel.tsx';
import { EmblaCarouselType, EmblaOptionsType } from 'embla-carousel';
import { useCallback, useEffect, useState } from 'react';
import useEmblaCarousel from 'embla-carousel-react';
import ClassNames from 'embla-carousel-class-names';

const OPTIONS: EmblaOptionsType = {
    breakpoints: {
        '(max-width: 600px)': {
            // Small screens (Mobile)
            align: 'center',
            slidesToScroll: 1,
        },
        '(min-width: 600px) and (max-width: 1500px)': {
            // Medium screens (Tablets)
            align: 'center',
            slidesToScroll: 3,
        },
        '(min-width: 1500px)': {
            // Large screens (Desktops)
            align: 'center',
            slidesToScroll: 4,
        },
    },
};

export default function jurySection() {
    const [emblaRef, emblaApi] = useEmblaCarousel(OPTIONS, [ClassNames()]);
    const [progress, setProgress] = useState(0);
    const logEmblaEvent = useCallback((emblaApi: EmblaCarouselType) => {
        console.log(emblaApi.scrollProgress());
        setProgress(emblaApi.scrollProgress());
        if (!emblaApi.canScrollNext()) {
            const element = document.querySelector('#jury');
            if (element) {
                element.classList.remove('ml-auto');
                element.classList.add('m-auto');
            }
        } else {
            const element = document.querySelector('#jury');

            if (element) {
                element.classList.remove('m-auto');
                element.classList.add('ml-auto');
            }
        }
    }, []);

    useEffect(() => {
        if (emblaApi) emblaApi.on('slidesInView', logEmblaEvent);
    }, [emblaApi, logEmblaEvent]);

    const SLIDES = jury.map((mentor, index) => (
        <JuryModule imgSrc={mentor.picture} name={mentor.name} company={mentor.company} job={mentor.job} key={index} />
    ));

    return (
        <div className="bg-[#000912] py-10 relative">
            <div className=" space-y-7 font-mont sm:w-11/12 w-11/12 z-10 relative m-auto">
                <img src="/jury/jury_title.svg"></img>
                {/* <img className="w-[90%]" src="/jury/jury_page_break.svg"></img> */}
                <div className="w-full  h-2 rounded-full overflow-hidden relative">
                    <div
                        className="h-full bg-white  transition-all duration-500"
                        style={{
                            width: `${(progress + 0.12) * 100}%`,
                        }}
                    ></div>
                    <hr></hr>
                </div>
            </div>
            <div id="jury" className="ml-auto space-y-7 py-10 sm:w-11/12 w-11/12 z-10">
                <EmblaCarousel
                    type="jury"
                    slides={SLIDES}
                    options={OPTIONS}
                    emblaRefs={emblaRef}
                    emblaApis={emblaApi}
                />
            </div>
        </div>
    );
}
