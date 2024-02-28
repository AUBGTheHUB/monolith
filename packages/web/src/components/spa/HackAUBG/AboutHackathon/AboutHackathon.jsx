import React from 'react';
import styles from './about_hackathon.module.css';

export const AboutHackathon = () => {
    return (
        <div className={styles.about_container_hack_aubg} id="about">
            <h1 className={styles.about_title_hack_aubg}>ABOUT</h1>
            <div className={styles.about_text_container_hack_aubg}>
                <p className={styles.about_text_hack_aubg}>
                    Welcome to HackAUBG 5.0 - the ultimate 52-hour hackathon experience organized by The Hub. At
                    HackAUBG, our goal is to provide a platform for students, professionals, and entrepreneurs to come
                    together and develop solutions for real-world problems. Whether you’re a programmer, a designer, or
                    simply have an interest in tech or business, we welcome you to join us and put your skills to the
                    test.
                    <br />
                    <br />
                    Over the course of 52 hours, you will work in teams to brainstorm and prototype your project idea
                    based on the topic we will reveal during the Opening Ceremony, as well as pitch your project to a
                    panel of judges. But you won’t be on your own - we will have a team of experienced mentors on hand
                    to offer guidance and support throughout the event. Plus, there will be awesome prizes and food to
                    keep you fueled and motivated!
                    <br />
                    <br />
                    HackAUBG is more than just a hackathon - it’s a community of innovators, collaborators, and
                    problem-solvers. We believe that together, we can create a better future through technology and
                    creativity.
                </p>
            </div>
        </div>
    );
};
