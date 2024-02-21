import React from 'react';
import { FAQModule } from './FAQModule';
import styles from './faq_section.module.css';
import data from './data.json';

export const FAQSection = () => {
    return (
        <div className={styles['faq-section']} id="faq">
            <img
                className={styles['left-svg']}
                src="FAQ-left.png"
                width="385"
                height="619"
                viewBox="0 0 385 619"
                fill="none"
            />

            <img className={styles['right-svg']} src="FAQ-right.png" />
            <h1 className={styles['faq-h1']}>FREQUENTLY ASKED QUESTIONS</h1>
            <div className={styles['faq']}>
                {data.map(data => (
                    <FAQModule id={data.id} title={data.title} text={data.text} key={data.title} />
                ))}
            </div>
        </div>
    );
};
