/* eslint-disable no-unused-vars */
import React from 'react';
import { MemberCard } from './MemberCard';
import { FaBeer } from 'react-icons/fa';
import { useState } from 'react';

export const Carousel = ({ props }) => {
    if (props && props.length != 0) {
        const [sliceIndex, setSliceIndex] = useState(0);

        console.log(`Props len ${props.length}`);

        const [firstSlide, setFirstSlide] = useState(
            'carousel-container-slider'
        );

        const [secondSlide, setSecondSlide] = useState(
            'carousel-container-slider-hidden'
        );

        const [firstMap, setFirstMap] = useState(
            props.slice(sliceIndex, sliceIndex + 3)
        );
        console.log(
            '🚀 ~ file: Carousel.jsx:24 ~ Carousel ~ firstMap',
            firstMap
        );

        const [secondMap, setSecondMap] = useState(
            props.slice(sliceIndex + 3, sliceIndex + 6)
        );

        console.log(
            '🚀 ~ file: Carousel.jsx:29 ~ Carousel ~ secondMap',
            secondMap
        );

        const slide = (className) => {
            setFirstSlide('carousel-container-slider left');
            setSecondSlide('carousel-container-slider animate');

            setTimeout(() => {
                try {
                    setSliceIndex(sliceIndex + 3);
                    setFirstMap(props.slice(sliceIndex + 3, sliceIndex + 6));
                    setSecondMap(props.slice(sliceIndex + 6, sliceIndex + 9));
                    setFirstSlide('carousel-container-slider');
                    setSecondSlide('carousel-container-slider-hidden');
                    console.log('HERE');
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
