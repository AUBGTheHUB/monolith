import React from 'react';
import { useState } from 'react';
import { AiOutlineArrowDown } from 'react-icons/ai';
import { AiOutlineArrowUp } from 'react-icons/ai';
import './journey_mobile.css';

export const JourneyStep = (props) => {
    // const [stepTitle, setStepTitle] = useState('container-title-not-displayed');
    const [stepContent, setStepContent] = useState(
        'container-content-not-displayed'
    );
    const [arrowDown, setArrowDown] = useState('journey-arrow-displayed');
    const [arrowUp, setArrowUp] = useState('journey-arrow-not-displayed');

    const setMenuClass = () => {
        if (stepContent == 'container-content-displayed') {
            setStepContent('container-content-not-displayed');
            setArrowDown('journey-arrow-displayed');
            setArrowUp('journey-arrow-not-displayed');

            console.log('not');
        } else {
            setStepContent('container-content-displayed');
            setArrowDown('journey-arrow-not-displayed');
            setArrowUp('journey-arrow-displayed');
            console.log('disp');
        }
    };

    return (
        <div
            className="mobile-step-container"
            onClick={() => {
                setMenuClass();
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

            <div className={stepContent}>{props.text}</div>
        </div>
    );
};
