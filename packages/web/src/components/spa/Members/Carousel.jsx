/* eslint-disable no-unused-vars */
import React from 'react';
import { MemberCard } from './MemberCard';
import { FaBeer } from 'react-icons/fa';
import { useState } from 'react';

export const Carousel = ({ props }) => {
    // props is a list of 6 items
    // first three are shown
    // second three are cached

    const [firstSlide, setFirstSlide] = useState('carousel-container-slider');

    const [secondSlide, setSecondSlide] = useState(
        'carousel-container-slider-hidden'
    );

    console.log(props);

    // if props empty don't load component

    const changeClassName = (className) => {
        if (className === 'carousel-container-slider') {
            return 'carousel-container-slider left';
        } else if (className === 'carousel-container-slider-hidden') {
            return 'carousel-container-slider animate';
        }
    };

    return (
        <div className="carousel-container">
            <FaBeer
                className="carousel-arrow-left"
                onClick={() => {
                    setFirstSlide(changeClassName(firstSlide));
                    setSecondSlide(changeClassName(secondSlide));
                }}
            />
            <div className="carousel-container-slider-holder">
                <div className={firstSlide}>
                    <MemberCard props={props[0]} />
                    <MemberCard props={props[0]} />
                    <MemberCard props={props[0]} />
                </div>
                <div className={secondSlide}>
                    <MemberCard props={props[1]} />
                    <MemberCard props={props[1]} />
                    <MemberCard props={props[1]} />
                </div>
            </div>
            <FaBeer className="carousel-arrow-right" onClick={() => {}} />
        </div>
    );
};
