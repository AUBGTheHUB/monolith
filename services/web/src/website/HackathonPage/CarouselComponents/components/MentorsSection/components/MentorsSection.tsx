import JuryModule from '../../../JuryAndMentorModule';
import mentors from '../StaticContent/mentors.json';
import '@/components/EmblaCarousel/SlidesPerViewCarousel/css/base.css';
import '@/components/EmblaCarousel/SlidesPerViewCarousel/css/embla-jury.css';
import EmblaCarousel from '@/components/EmblaCarousel/SlidesPerViewCarousel/js/EmblaCarousel.tsx';
import { EmblaCarouselType } from 'embla-carousel';
import { useCallback, useEffect, useState } from 'react';
import useEmblaCarousel from 'embla-carousel-react';
import ClassNames from 'embla-carousel-class-names';
import { OPTIONS } from '../../../JudgesAndMentorsOptions';

export default function MentorsSection() {
    const [emblaRef, emblaApi] = useEmblaCarousel(OPTIONS, [ClassNames()]);
    const [progress, setProgress] = useState(0);
    const logEmblaEvent = useCallback((emblaApi: EmblaCarouselType) => {
        setProgress(emblaApi.scrollProgress());
        if (!emblaApi.canScrollNext()) {
            const element = document.querySelector('#mentors');
            if (element) {
                element.classList.remove('ml-auto');
                element.classList.add('m-auto');
            }
        } else {
            const element = document.querySelector('#mentors');

            if (element) {
                element.classList.remove('m-auto');
                element.classList.add('ml-auto');
            }
        }
    }, []);

    useEffect(() => {
        if (emblaApi) emblaApi.on('slidesInView', logEmblaEvent);
    }, [emblaApi, logEmblaEvent]);

    const SLIDES = mentors.map((mentor, index) => (
        <JuryModule imgSrc={mentor.picture} name={mentor.name} company={mentor.company} job={mentor.job} key={index} />
    ));

    return (
        <div className="bg-[#000912] py-10 relative">
            <div className=" space-y-7 font-mont sm:w-11/12 w-11/12 z-10 relative m-auto">
                <div className="sm:text-4xl text-3xl sm:mb-20 mb-10 flex items-center ">
                    <img src="./n.png" alt="" className="w-[1.6rem]" />
                    <p className="text-white ml-5 tracking-[0.2em]">MENTORS</p>
                </div>
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
            <div id="mentors" className="ml-auto space-y-7 py-10 sm:w-11/12 w-11/12 z-10">
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
