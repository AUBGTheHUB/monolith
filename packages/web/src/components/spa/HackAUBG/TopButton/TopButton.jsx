import React, { useState } from 'react';
import './top_button.css';

export const TopButton = () => {
    const [visible, setVisibility] = useState(false);

    const toggleVisibility = () => {
        const scrolled = document.documentElement.scrollTop;

        if (scrolled > 300) {
            setVisibility(true);
        } else if (scrolled <= 300) {
            setVisibility(false);
        }
    };

    const scrollToTop = () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    };

    window.addEventListener('scroll', toggleVisibility);

    return (
        <a href="#">
            <div
                className="hackaubg-top-button"
                onClick={scrollToTop}
                style={{ display: visible ? 'inline' : 'none' }}
            >
                🡅
            </div>
        </a>
    );
};
