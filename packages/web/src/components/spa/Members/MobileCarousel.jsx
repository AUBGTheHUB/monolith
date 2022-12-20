/* eslint-disable no-unused-vars */
import React from 'react';
import { useState } from 'react';
import { MemberCard } from './MemberCard';
import { BsChevronDoubleRight as ArrowIcon } from 'react-icons/bs';

export const MobileCarousel = ({ props }) => {
    const [currentIndex, setCurrentIndex] = useState(0);

    const getLeftMember = (current) => {
        if (currentIndex - 1 < 0) {
            setCurrentIndex(props.length - 1);
        } else {
            setCurrentIndex(currentIndex - 1);
        }
    };

    const getRightMember = () => {
        if (currentIndex + 1 <= props.length - 1) {
            setCurrentIndex(currentIndex + 1);
        } else {
            setCurrentIndex(0);
        }
    };

    return (
        <div className="mobile-carousel-container">
            <ArrowIcon
                className="carousel-arrow-left mobile"
                onClick={getLeftMember}
            />
            <div className="mobile-carousel-container-moving">
                <MemberCard
                    props={props[currentIndex]}
                    animationClassname={'members-card-hover-overlay'}
                />
            </div>
            <ArrowIcon
                className="carousel-arrow-right mobile"
                onClick={getRightMember}
            />
        </div>
    );
};
