import React from 'react';
import { useState } from 'react';
import { useEffect } from 'react';
import './landing_animation.css';

export const MatrixWindow = () => {
    const [dataValue, setDataValue] = useState('HACKAUBG 5.0');
    const [clicks, setClicks] = useState(0);

    useEffect(() => {
        if (clicks >= 69) {
            setDataValue('TONI MONTANA');
        }
    }, [clicks]);

    const animateLetters = () => {
        const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        let interval = null;
        const h1 = document.querySelector('.hackaubg-moving-letters');

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

            iteration += 1 / 4.5;
        }, 30);
    };

    useEffect(animateLetters, []);

    return (
        <div className="hackaubg-landing-section-text-animation-container">
            <div className="hackaubg-landing-content">
                <h1
                    data-value={dataValue}
                    className="hackaubg-moving-letters"
                    onMouseEnter={() => {
                        animateLetters();
                        setClicks(clicks + 1);
                    }}
                >
                    HACKAUBG 5.0
                </h1>
                <p>31st March - 2nd April, AUBG - Blagoevgrad</p>
                <button
                    className="Reg-btn"
                    onClick={() => {
                        window.location.href = '#registration';
                    }}
                >
                    Go to Registration
                </button>
            </div>
        </div>
    );
};
