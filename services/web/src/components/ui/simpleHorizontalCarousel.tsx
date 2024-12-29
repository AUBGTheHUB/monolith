import React, { useState } from 'react';

interface CarouselProps {
    items: React.ReactNode[]; // Array of React nodes (e.g., strings, JSX elements)
    itemsPerSlide: number; // Number of items per slide
}

// Utility to chunk an array into smaller arrays
function chunkArray<T>(array: T[], size: number): T[][] {
    return array.reduce((acc, _, i) => {
        if (i % size === 0) acc.push(array.slice(i, i + size));
        return acc;
    }, [] as T[][]);
}

// Slide component to display items in a single slide
const Slide: React.FC<{ items: React.ReactNode[] }> = ({ items }) => {
    return (
        <div className="flex justify-center content-center flex-row gap-2 snap-start w-full shrink-0">{...items}</div>
    );
};

// Carousel Component
const SimpleHorizontalCarousel: React.FC<CarouselProps> = ({ items, itemsPerSlide }) => {
    const [currentSlide, setCurrentSlide] = useState(0);
    const slideComponents = chunkArray(items, itemsPerSlide);

    // Logic to set the correct current slide number when scrolling through the slides
    const scrollHandler = (e: React.UIEvent<HTMLDivElement>) => {
        const scrollLeft = e.currentTarget.scrollLeft; // Distance scrolled starting from the beginning of the horizontal scrollable element (from the left side)
        const containerWidth = e.currentTarget.offsetWidth; // Width of the container
        const newCurrentSlide = Math.round(scrollLeft / containerWidth); // Calculate the new current slide index
        setCurrentSlide(newCurrentSlide);
    };

    return (
        <div className="border">
            {/* Carousel Container */}
            <div
                className="flex overflow-x-scroll snap-x snap-mandatory scroll-smooth scrollbar-hide w-full"
                onScroll={scrollHandler}
            >
                {slideComponents.map((slideItems, index) => (
                    <Slide items={slideItems} key={index} />
                ))}
            </div>

            {/* Dots Indicator */}
            <div className="flex justify-center mt-4">
                {slideComponents.map((_, index) => (
                    <div
                        className={`w-2 h-2 mx-1 rounded-full cursor-pointer ${
                            currentSlide === index ? 'bg-gray-400' : 'bg-gray-200'
                        }`}
                        key={index}
                    ></div>
                ))}
            </div>
        </div>
    );
};

export default SimpleHorizontalCarousel;
