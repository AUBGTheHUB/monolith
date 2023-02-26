import React from 'react';
import './landing_animation.css';

export const MatrixWindow = () => {
    // window.onload = function () {
    //     const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

    //     let interval = null;

    //     document.querySelector('h1').onmouseover = (event) => {
    //         let iteration = 0;

    //         clearInterval(interval);

    //         interval = setInterval(() => {
    //             event.target.innerText = event.target.innerText
    //                 .split('')
    //                 .map((letter, index) => {
    //                     if (index < iteration) {
    //                         return event.target.dataset.value[index];
    //                     }

    //                     return letters[Math.floor(Math.random() * 26)];
    //                 })
    //                 .join('');

    //             if (iteration >= event.target.dataset.value.length) {
    //                 clearInterval(interval);
    //             }

    //             iteration += 1 / 3;
    //         }, 30);
    //     };
    // };
    window.onload = function () {
        const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        let interval = null;
        const h1 = document.querySelector('h1');

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

        h1.addEventListener('mouseover', startAnimation);
        startAnimation({ target: h1 });
    };
    return (
        <div className="animation-container">
            <div className="landing-content">
                <h1 data-value="HACKAUBG 5.0">HACKAUBG 5.0</h1>
                <p>31st March - 2nd April, AUBG - Blagoevgrad</p>
                <button className="Reg-btn">Go to Registration</button>
            </div>
        </div>
    );
};
