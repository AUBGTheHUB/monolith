import React from 'react';
import './landing_animation.css';
// import { InvokeAnimation } from './InvokeAnimation';
// import './matrix.gif';

export const MatrixWindow = () => {
    return (
        <div className="animation-container">
            <div className="landing-content">
                <div className="landing-text">
                    <h1>HackAUBG</h1>
                    <p>31st March - 2nd April, AUBG - Blagoevgrad</p>
                </div>
                <button className="Reg-btn">Go to Registration</button>
            </div>
            {/* <canvas>
                <InvokeAnimation/>
            </canvas> */}
            {/* <img
                    src="gif.gif"
                    className="matrix-image"
                    alt="Matrix animation"
                /> */}
        </div>
    );
};
