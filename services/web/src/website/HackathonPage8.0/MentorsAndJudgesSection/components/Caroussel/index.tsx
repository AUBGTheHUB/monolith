import { cn } from '@/lib/utils';
import { Judge } from '@/types/judge';
import { Mentor } from '@/types/mentor';
import type { EmblaOptionsType } from 'embla-carousel';
import ClassNames from 'embla-carousel-class-names';
import useEmblaCarousel from 'embla-carousel-react';
import { useCallback, useEffect, useState } from 'react';
import { CarousselButton } from '../CarousselButton';
import { MentorsAndJudgesCard } from '../MentorsAndJudgesCard';
import './index.css';

const OPTIONS: EmblaOptionsType = {
    loop: false,
    align: 'center',
    breakpoints: {
        '(max-width: 800px)': {
            // Small screens (Mobile)
            align: 'center',
            slidesToScroll: 1,
        },
        '(min-width: 800px) and (max-width: 1500px)': {
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

type CarouselProps<T extends Mentor | Judge> = {
    title: string;
    imgSrc: string;
    className?: string;
    data?: T[];
};

export function Carousel<T extends Mentor | Judge>({ className, title, imgSrc, data }: CarouselProps<T>) {
    const [emblaRef, emblaApi] = useEmblaCarousel(OPTIONS, [ClassNames()]);

    const goToPrev = useCallback(() => emblaApi?.scrollPrev(), [emblaApi]);
    const goToNext = useCallback(() => emblaApi?.scrollNext(), [emblaApi]);

    const [canPrev, setCanPrev] = useState(false);
    const [canNext, setCanNext] = useState(false);

    useEffect(() => {
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
        <div
            className={cn('embla flex justify-center flex-col gap-8 w-full mx-auto px-8 md:px-0', className)}
            style={{ maxWidth: 'clamp(40rem, 82vw, 80rem)' }}
        >
            {/* HEADER */}

            <div className="flex flex-col sm:flex-row items-center justify-between">
                <div className="flex items-center gap-[5px]">
                    <img src={imgSrc} alt="Hunger Games Pin" className="h-[42px] w-auto" />
                    <h2 className="font-orbitron text-[40px] leading-[1] tracking-[0.3em] text-[#FFFDF5]">{title}</h2>
                </div>

                <div className="hidden sm:flex justify-center gap-3">
                    <CarousselButton left onClick={goToPrev} disabled={!canPrev} />
                    <CarousselButton right onClick={goToNext} disabled={!canNext} />
                </div>
            </div>

            {/* CAROUSEL */}

            <div className={cn('embla__viewport')} ref={emblaRef}>
                <div className="embla__container">
                    {data ? (
                        data?.map((element, idx) => (
                            <div
                                className={cn(
                                    'embla__slide',
                                    'ease-linear duration-200',
                                    !data ? 'opacity-0' : 'opacity-100',
                                )}
                                key={idx}
                            >
                                <MentorsAndJudgesCard {...element} isLoading={!!data} />
                            </div>
                        ))
                    ) : (
                        <MentorsAndJudgesCard name="Loading..." company="" avatar_url="" />
                    )}
                </div>
            </div>
        </div>
    );
}
