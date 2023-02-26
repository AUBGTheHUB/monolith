import React from 'react';
import { useEffect } from 'react';
import './landing_animation.css';

export const MatrixWindow = () => {
    const animateLetters = () => {
        const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        let interval = null;
        const h1 = document.querySelector('.toni-montana');

        let iteration = 0;
        clearInterval(interval);

        interval = setInterval(() => {
            h1.innerText = h1.innerText
                .split('')
                .map((letter, index) => {
                    if (index < iteration) {
                        return h1.dataset.value[index];
                    }

                    return letters[Math.floor(Math.random() * 26)];
                })
                .join('');

            if (iteration >= h1.dataset.value.length) {
                clearInterval(interval);
            }

            iteration += 1 / 3;
        }, 30);
    };

    useEffect(animateLetters, []);

    return (
        <div className="hackaubg-landing-section-text-animation-container">
            <div className="hackaubg-landing-content">
                <h1
                    data-value="HACKAUBG 5.0"
                    className="toni-montana"
                    onMouseEnter={animateLetters}
                >
                    HACKAUBG 5.0
                </h1>
                <p>31st March - 2nd April, AUBG - Blagoevgrad</p>
                <button className="Reg-btn">Go to Registration</button>
            </div>
        </div>
    );
};
