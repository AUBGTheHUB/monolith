import React from 'react';
import { EmblaCarouselType, EmblaOptionsType } from 'embla-carousel';
import { DotButton, useDotButton } from './EmblaCarouselDotButton.tsx';
import { PrevButton, NextButton, usePrevNextButtons } from './EmblaCarouselArrowButtons.tsx';
import useEmblaCarousel, { EmblaViewportRefType } from 'embla-carousel-react';
import ClassNames from 'embla-carousel-class-names';

/*
Embla Carousel is a lightweight library for creating Carousels in react
Learn more about it: https://www.embla-carousel.com/
This folliwng implementation is based on 'Slides Per View' example:
https://www.embla-carousel.com/examples/predefined/#slides-per-view

They have a couple more very useful examples that you can use, which you can
check in their website.
*/

type PropType = {
    slides: React.ReactNode[] | React.ReactNode[][];
    emblaApis?: EmblaCarouselType | undefined;
    options?: EmblaOptionsType;
    type: string;
    emblaRefs?: EmblaViewportRefType;
};

const EmblaCarousel: React.FC<PropType> = (props) => {
    const { slides, options, type, emblaRefs, emblaApis } = props;
    let emblaRef, emblaApi;
    if (!emblaRefs && !emblaApis) {
        [emblaRef, emblaApi] = useEmblaCarousel(options, [ClassNames()]);
    } else {
        emblaRef = emblaRefs;
        emblaApi = emblaApis;
    }
    const emblaClass = 'embla ' + type;
    const { selectedIndex, scrollSnaps, onDotButtonClick } = useDotButton(emblaApi);

    const { prevBtnDisabled, nextBtnDisabled, onPrevButtonClick, onNextButtonClick } = usePrevNextButtons(emblaApi);
    return (
        <section className={emblaClass}>
            <div className="embla__viewport" ref={emblaRef}>
                <div className="embla__container">
                    {type == 'team' &&
                        Array.isArray(slides[0]) &&
                        (slides as React.ReactNode[][]).map((slide: React.ReactNode[], index) => (
                            <div className="embla__slide" key={index}>
                                <div className="embla__slide__inner">{slide[0]}</div>
                                <div className="embla__slide__inner">{slide[1]}</div>
                            </div>
                        ))}
                    {type == 'jury' &&
                        slides.map((slide, index) => (
                            <div className="embla__slide " key={index}>
                                {slide}
                            </div>
                        ))}
                </div>
            </div>

            <div className="embla__controls">
                <div className="embla__buttons">
                    <PrevButton onClick={onPrevButtonClick} disabled={prevBtnDisabled} />
                    <NextButton onClick={onNextButtonClick} disabled={nextBtnDisabled} />
                </div>

                <div className="embla__dots">
                    {scrollSnaps.map((_, index) => (
                        <DotButton
                            key={index}
                            onClick={() => onDotButtonClick(index)}
                            className={'embla__dot'.concat(index === selectedIndex ? ' embla__dot--selected' : '')}
                        />
                    ))}
                </div>
            </div>
        </section>
    );
};

export default EmblaCarousel;
