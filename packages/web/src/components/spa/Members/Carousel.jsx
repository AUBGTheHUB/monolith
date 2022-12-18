/* eslint-disable no-unused-vars */
import React from 'react';
import { MemberCard } from './MemberCard';
import { FaBeer } from 'react-icons/fa';
import { useState } from 'react';

export const Carousel = ({ props }) => {
    if (props && props.length != 0) {
        const [sliceIndex, setSliceIndex] = useState(0);

        const [firstSlide, setFirstSlide] = useState(
            'carousel-container-slider'
        );

        const [secondSlide, setSecondSlide] = useState(
            'carousel-container-slider-hidden'
        );

        const [firstMap, setFirstMap] = useState(
            props.slice(sliceIndex, sliceIndex + 3)
        );

        // console.log(
        //     '🚀 ~ file: Carousel.jsx:24 ~ Carousel ~ firstMap',
        //     firstMap
        // );

        const [secondMap, setSecondMap] = useState(
            props.slice(sliceIndex + 3, sliceIndex + 6)
        );

        // console.log(
        //     '🚀 ~ file: Carousel.jsx:29 ~ Carousel ~ secondMap',
        //     secondMap
        // );

        const increaseSlice = (currentPosIndex, setter) => {
            console.log(
                '🚀 ~ file: Carousel.jsx:40 ~ increaseSlice ~ currentPosIndex',
                currentPosIndex
            );

            if (currentPosIndex + 6 === props.length) {
                setter(
                    props
                        .slice(currentPosIndex + 3, currentPosIndex + 5)
                        .append(props[0])
                );
                return 1;
            } else if (currentPosIndex + 5 === props.length) {
                setter(
                    props
                        .slice(currentPosIndex + 3, currentPosIndex + 4)
                        .concat(props.slice(0, 2))
                );
                return 2;
            } else if (currentPosIndex + 4 === props.length) {
                setter(props.slice(0, 3));
                return 3;
            } else {
                setter(props.slice(currentPosIndex + 3, currentPosIndex + 6));
                return currentPosIndex + 6;
            }
        };

        const slide = (className) => {
            setFirstSlide('carousel-container-slider left');
            setSecondSlide('carousel-container-slider animate');

            setTimeout(() => {
                try {
                    setSliceIndex(
                        increaseSlice(
                            increaseSlice(sliceIndex, setFirstMap),
                            setSecondMap
                        )
                    );

                    setFirstSlide('carousel-container-slider');
                    setSecondSlide('carousel-container-slider-hidden');
                } catch (error) {
                    console.log(error);
                }
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
