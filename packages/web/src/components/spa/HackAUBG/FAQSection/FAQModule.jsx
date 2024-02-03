import React from 'react';
import { useState } from 'react';
import { AiOutlinePlus } from 'react-icons/ai';
import { AiOutlineMinus } from 'react-icons/ai';
import './faq_module.css';

export const FAQModule = props => {
    const [stepContent, setStepContent] = useState('faq-container-content-not-displayed');
    // eslint-disable-next-line no-unused-vars
    const [stepId, setStepId] = useState(`faq-step-${props.id}`);
    const [arrowDown, setArrowDown] = useState('faq-arrow-displayed');
    const [arrowUp, setArrowUp] = useState('faq-arrow-not-displayed');
    const getHeight = () => {
        var divElement = document.getElementById(stepId);
        if (divElement) {
            return divElement.scrollHeight;
        }
    };

    const setMenuClass = () => {
        if (stepContent == 'faq-container-content-displayed') {
            setStepContent('faq-container-content-not-displayed');
            setArrowDown('faq-arrow-displayed');
            setArrowUp('faq-arrow-not-displayed');
        } else {
            setStepContent('faq-container-content-displayed');
            setArrowDown('faq-arrow-not-displayed');
            setArrowUp('faq-arrow-displayed');
        }
    };

    return (
        <div style={{ '--elem-Height': getHeight() + 'px' }} className="faq-mobile-step-container">
            <div
                className="faq-step-title"
                onClick={() => {
                    setMenuClass();
                    getHeight();
                }}>
                <div className="faq-h2">
                    <h2>{props.stepnum}</h2>
                    <h2>{props.title}</h2>
                </div>

                <div className={arrowUp}>
                    <AiOutlineMinus />
                </div>
                <div className={arrowDown}>
                    <AiOutlinePlus />
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
