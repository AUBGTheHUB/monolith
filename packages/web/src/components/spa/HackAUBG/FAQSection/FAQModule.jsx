import React from 'react';
import { useState } from 'react';
import { AiOutlinePlus } from 'react-icons/ai';
import { AiOutlineMinus } from 'react-icons/ai';
import styles from './faq.module.css';

export const FAQModule = props => {
    const [stepContent, setStepContent] = useState(styles.faqcontainercontentnotdisplayed);
    // eslint-disable-next-line no-unused-vars
    const [stepId, setStepId] = useState(`faq-step${props.id}`);
    const [arrowDown, setArrowDown] = useState(styles.faqarrowdisplayed);
    const [arrowUp, setArrowUp] = useState(styles.faqarrownotdisplayed);

    const getHeight = () => {
        const divElement = document.getElementById(stepId);
        if (divElement) {
            document.documentElement.style.setProperty(`--elem-Height`, `${divElement.scrollHeight}px`);
        }
    };

    const setMenuClass = () => {
        if (stepContent == styles.faqcontainercontentdisplayed) {
            setStepContent(styles.faqcontainercontentnotdisplayed);
            setArrowDown(styles.faqarrowdisplayed);
            setArrowUp(styles.faqarrownotdisplayed);
        } else {
            setStepContent(styles.faqcontainercontentdisplayed);
            setArrowDown(styles.faqarrownotdisplayed);
            setArrowUp(styles.faqarrowdisplayed);
        }
    };
    return (
        <div className={styles.faqmobilestepcontainer}>
            <div
                className={styles.faqsteptitle}
                onClick={() => {
                    setMenuClass();
                    getHeight();
                }}>
                <div className={styles.faqh2}>
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
