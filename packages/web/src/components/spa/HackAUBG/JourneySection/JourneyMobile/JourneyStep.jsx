import React from 'react';
import { useState } from 'react';
import { AiOutlineArrowDown } from 'react-icons/ai';
import { AiOutlineArrowUp } from 'react-icons/ai';
import './journey_mobile.css';

export const JourneyStep = (props) => {
    const [stepContent, setStepContent] = useState(
        'container-content-not-displayed'
    );
    // eslint-disable-next-line no-unused-vars
    const [stepId, setStepId] = useState(`step-${props.id}`);
    const [arrowDown, setArrowDown] = useState('journey-arrow-displayed');
    const [arrowUp, setArrowUp] = useState('journey-arrow-not-displayed');
    const getHeight = () => {
        var divElement = document.getElementById(stepId);
        if (divElement) {
            console.log(divElement.scrollHeight);

            return divElement.scrollHeight;
        }
    };

    const setMenuClass = () => {
        if (stepContent == 'container-content-displayed') {
            setStepContent('container-content-not-displayed');
            setArrowDown('journey-arrow-displayed');
            setArrowUp('journey-arrow-not-displayed');
        } else {
            setStepContent('container-content-displayed');
            setArrowDown('journey-arrow-not-displayed');
            setArrowUp('journey-arrow-displayed');
        }
    };

    return (
        <div
            style={{ '--elem-Height': getHeight() + 'px' }}
            className="mobile-step-container"
        >
            <div
                className="step-title"
                onClick={() => {
                    setMenuClass();
                    getHeight();
                }}
            >
                <div className="journey-h2">
                    <h2>{props.stepnum}</h2>
                    <h2>{props.title}</h2>
                </div>

                <div className={arrowUp}>
                    <AiOutlineArrowUp />
                </div>
                <div className={arrowDown}>
                    <AiOutlineArrowDown />
                </div>
            </div>

            <div className={stepContent} id={stepId}>
                <div>
                    <p>{props.text}</p>
                </div>
            </div>
        </div>
    );
};
