import type { EmblaOptionsType } from 'embla-carousel';
import useEmblaCarousel from 'embla-carousel-react';
import * as React from 'react';
import { cn } from '@/lib/utils';
import ClassNames from 'embla-carousel-class-names';
import { CarousselButton } from '../CarousselButton';
import { MentorsAndJudgesCard } from '../MentorsAndJudgesCard';
import './index.css';

export const OPTIONS: EmblaOptionsType = {
    loop: false,
    align: 'center',
    breakpoints: {
        '(max-width: 600px)': {
            // Small screens (Mobile)
            align: 'center',
            slidesToScroll: 1,
        },
        '(min-width: 600px) and (max-width: 1500px)': {
            // Medium screens (Tablets)
            align: 'center',
            slidesToScroll: 'auto',
        },
        '(min-width: 1500px)': {
            // Large screens (Desktops)
            align: 'center',
            slidesToScroll: 4,
        },
    },
};

type CarouselProps = {
    title: string;
    imgSrc: string;
    className?: string;
    slides?: number;
};

export function Carousel({ className, title, slides = 12, imgSrc }: CarouselProps) {
    const [emblaRef, emblaApi] = useEmblaCarousel(OPTIONS, [ClassNames()]);

    const goToPrev = React.useCallback(() => emblaApi?.scrollPrev(), [emblaApi]);
    const goToNext = React.useCallback(() => emblaApi?.scrollNext(), [emblaApi]);

    // Optional: keep buttons in sync with embla state (works even with loop=true)
    const [canPrev, setCanPrev] = React.useState(false);
    const [canNext, setCanNext] = React.useState(false);

    React.useEffect(() => {
        if (!emblaApi) return;

        const update = () => {
            setCanPrev(emblaApi.canScrollPrev());
            setCanNext(emblaApi.canScrollNext());
        };

        update();
        emblaApi.on('select', update);
        emblaApi.on('reInit', update);

        return () => {
            emblaApi.off('select', update);
            emblaApi.off('reInit', update);
        };
    }, [emblaApi]);

    return (
        <div className={cn('embla flex justify-center flex-col gap-8 w-full sm:px-16 md:px-28 xl:px-40', className)}>
            {/* HEADER */}

            <div className="flex flex-col sm:flex-row items-center justify-between">
                <div className="flex flex-row items-center gap-[18px]">
                    <img src={imgSrc} alt="Judges Pin" className="h-[42px] w-auto" />
                    <span className="text-[40px] font-orbitron tracking-widest">{title}</span>
                </div>

                <div className="hidden sm:flex justify-center gap-3">
                    <CarousselButton left onClick={goToPrev} disabled={!canPrev} />
                    <CarousselButton right onClick={goToNext} disabled={!canNext} />
                </div>
            </div>

            {/* CAROUSEL */}

            <div className="embla__viewport" ref={emblaRef}>
                <div className="embla__container sm:w-[600px] md:w-[900px] lg:w-[1100px]">
                    {Array.from({ length: slides }).map(
                        (
                            _,
                            idx, // TODO: replace after real data becomes available
                        ) => (
                            <div className="embla__slide" key={idx}>
                                <MentorsAndJudgesCard />
                            </div>
                        ),
                    )}
                </div>
            </div>
        </div>
    );
}
