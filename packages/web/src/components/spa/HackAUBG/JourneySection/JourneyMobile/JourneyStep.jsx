import React from 'react';
import { useState } from 'react';
import { AiOutlineArrowDown } from 'react-icons/ai';
import { AiOutlineArrowUp } from 'react-icons/ai';
import './journey_mobile.css';

export const JourneyStep = (props) => {
    const [stepTitle, setStepTitle] = useState('container-title-displayed');
    const [stepContent, setStepContent] = useState(
        'container-content-not-displayed'
    );

    return (
        <div className="mobile-step-container">
            <div
                className={stepTitle}
                onClick={() => {
                    setStepContent('container-content-displayed');
                    setStepTitle('container-title-not-displayed');
                }}
            >
                {props.title}
                <AiOutlineArrowDown />
            </div>
            <div
                className={stepContent}
                onClick={() => {
                    setStepContent('container-content-not-displayed');
                    setStepTitle('container-title-displayed');
                }}
            >
                {props.title}
                <AiOutlineArrowUp />
                {props.text}
            </div>
        </div>
    );
};
