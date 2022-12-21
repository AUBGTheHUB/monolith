import React from 'react';
import { MemberCard } from './MemberCard';
import { BsChevronDoubleRight as ArrowIcon } from 'react-icons/bs';
import { useState } from 'react';
import { useRef } from 'react';

export const Carousel = ({ props }) => {
    if (props && props.length != 0) {
        const [sliceIndex, setSliceIndex] = useState(3);

        const [firstSlide, setFirstSlide] = useState(
            'carousel-container-slider'
        );

        const [hoverEffectEnabled, setHoverEffect] = useState(
            'members-card-hover-overlay'
        );

        const [secondSlide, setSecondSlide] = useState(
            'carousel-container-slider-hidden'
        );

        const [firstMap, setFirstMap] = useState(
            props.slice(sliceIndex - 3, sliceIndex)
        );

        const [secondMap, setSecondMap] = useState(
            props.slice(sliceIndex, sliceIndex + 3)
        );

        const increaseSlice = (currentPosIndex, setter) => {
            if (currentPosIndex === props.length) {
                setter(props.slice(0, 3));
                return 0;
            } else if (currentPosIndex + 1 === props.length) {
                let slicedList = [props[props.length - 1]].concat(
                    props.slice(0, 2)
                );
                setter(slicedList);
                return -1;
            } else if (currentPosIndex + 2 === props.length) {
                let slicedList = props
                    .slice(props.length - 2, props.length)
                    .concat(props[0]);
                setter(slicedList);
                return -2;
            } else if (currentPosIndex === -4) {
                let slicedList = [props[props.length - 1]].concat(
                    props.slice(0, 2)
                );
                setter(slicedList);
                return 2;
            } else if (currentPosIndex === -5) {
                let slicedList = props
                    .slice(props.length - 2, props.length)
                    .concat(props[0]);
                setter(slicedList);
                return 1;
            } else {
                setter(props.slice(currentPosIndex, currentPosIndex + 3));
                return currentPosIndex + 3;
            }
        };

        const runningSlicing = useRef(false);

        const slide = () => {
            console.log('HELLO WORLD');
            if (!runningSlicing.current) {
                runningSlicing.current = true;

                setHoverEffect('hidden');

                setFirstSlide('carousel-container-slider left');
                setSecondSlide('carousel-container-slider animate');

                setTimeout(() => {
                    var index = increaseSlice(sliceIndex, setFirstMap);
                    index = increaseSlice(index, setSecondMap);

                    if (index == 0) {
                        setSliceIndex(0);
                    } else {
                        setSliceIndex(index - 3);
                    }

                    setFirstSlide('carousel-container-slider');
                    setSecondSlide('carousel-container-slider-hidden');

                    runningSlicing.current = false;
                    setHoverEffect('members-card-hover-overlay');
                }, 1000);
            }
        };

        return (
            <div className="carousel-container">
                <ArrowIcon className="carousel-arrow-left" onClick={slide} />
                <div className="carousel-container-slider-holder">
                    <div className={firstSlide}>
                        {firstMap.map((member, index) => (
                            <MemberCard
                                props={member}
                                key={index}
                                animationClassname={hoverEffectEnabled}
                            />
                        ))}
                    </div>
                    <div className={secondSlide}>
                        {secondMap.map((member, index) => (
                            <MemberCard
                                props={member}
                                key={index}
                                animationClassname={hoverEffectEnabled}
                            />
                        ))}
                    </div>
                </div>
                <ArrowIcon className="carousel-arrow-right" onClick={slide} />
            </div>
        );
    }
};
