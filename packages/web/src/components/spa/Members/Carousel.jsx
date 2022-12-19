/* eslint-disable no-unused-vars */
import React from 'react';
import { MemberCard } from './MemberCard';
import { FaBeer } from 'react-icons/fa';
import { useState } from 'react';

export const Carousel = ({ props }) => {
    if (props && props.length != 0) {
        const [sliceIndex, setSliceIndex] = useState(3);

        const [firstSlide, setFirstSlide] = useState(
            'carousel-container-slider'
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
            } else {
                setter(props.slice(currentPosIndex, currentPosIndex + 3));
                return currentPosIndex + 3;
            }
        };

        const slide = (className) => {
            setFirstSlide('carousel-container-slider left');
            setSecondSlide('carousel-container-slider animate');

            setTimeout(() => {
                var index = increaseSlice(sliceIndex, setFirstMap);
                index = increaseSlice(index, setSecondMap);
                setSliceIndex(index);

                setFirstSlide('carousel-container-slider');
                setSecondSlide('carousel-container-slider-hidden');
            }, 1000);
        };

        return (
            <div className="carousel-container">
                <FaBeer className="carousel-arrow-left" onClick={slide} />
                <div className="carousel-container-slider-holder">
                    <div className={firstSlide}>
                        {firstMap.map((member, index) => (
                            <MemberCard props={member} key={index} />
                        ))}
                    </div>
                    <div className={secondSlide}>
                        {secondMap.map((member, index) => (
                            <MemberCard props={member} key={index} />
                        ))}
                    </div>
                </div>
                <FaBeer className="carousel-arrow-right" onClick={() => {}} />
            </div>
        );
    }
};
