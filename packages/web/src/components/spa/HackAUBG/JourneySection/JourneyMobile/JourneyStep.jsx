import React from 'react';
import { useState } from 'react';
import { AiOutlineArrowDown } from 'react-icons/ai';
import { AiOutlineArrowUp } from 'react-icons/ai';
import './journey_mobile.css';

export const JourneyStep = (props) => {
    const [stepContent, setStepContent] = useState(
        'container-content-not-displayed'
    );
    const [arrowDown, setArrowDown] = useState('journey-arrow-displayed');
    const [arrowUp, setArrowUp] = useState('journey-arrow-not-displayed');
    const getHeight = () => {
        const divElement = document.getElementById('test');
        if (divElement) {
            return divElement.scrollHeight;
        } else {
            return;
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
            style={{ '--elem-Height': getHeight() + 15 + 'px' }}
            className="mobile-step-container"
            onClick={() => {
                setMenuClass();
                getHeight();
            }}
        >
            <div className="smth">
                {props.title}
                <div className={arrowUp}>
                    <AiOutlineArrowUp />
                </div>
                <div className={arrowDown}>
                    <AiOutlineArrowDown />
                </div>
            </div>

            <div className={stepContent}>
                <div id="test">{props.text}</div>
            </div>
        </div>
    );
};
