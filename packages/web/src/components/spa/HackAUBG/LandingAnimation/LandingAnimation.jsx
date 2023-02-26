import React from 'react';
import { useEffect } from 'react';
import './landing_animation.css';

export const MatrixWindow = () => {
    useEffect(() => {
        const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        let interval = null;
        const title = document.getElementById('title');

        function startAnimation(event) {
            let iteration = 0;
            clearInterval(interval);

            interval = setInterval(() => {
                event.target.innerText = event.target.innerText
                    .split('')
                    .map((letter, index) => {
                        if (index < iteration) {
                            return event.target.dataset.value[index];
                        }

                        return letters[Math.floor(Math.random() * 26)];
                    })
                    .join('');

                if (iteration >= event.target.dataset.value.length) {
                    clearInterval(interval);
                }

                iteration += 1 / 3;
            }, 30);
        }

        if (title) {
            title.addEventListener('mouseover', startAnimation);
            startAnimation({ target: title });
        }

        return () => {
            if (title) {
                title.removeEventListener('mouseover', startAnimation);
            }
            clearInterval(interval);
        };
    }, []);

    return (
        <div className="animation-container">
            <div className="landing-content">
                <h1 data-value="HACKAUBG 5.0" id="title">
                    HACKAUBG 5.0
                </h1>
                <p>31st March - 2nd April, AUBG - Blagoevgrad</p>
                <button className="Reg-btn">Go to Registration</button>
            </div>
        </div>
    );
};
