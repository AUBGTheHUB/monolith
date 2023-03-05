import React from 'react';
import './faq_section.css';

export const FaqSection = () => {
    return (
        <div className="faq-container" id="faq">
            <h1 className="faq">Frequently Asked Questions</h1>
            <div className="faq-text-container">
                <h2 className="faq-header">
                    I want to participate! When is the deadline for registering?
                </h2>
                <p className="faq-text">
                    Registration is open until Friday, March 25th.
                </p>
                <h2 className="faq-header">
                    How many people can be in a team?
                </h2>
                <p className="faq-text">
                    The minimum number of people in a team is 3, but you can
                    have up to 6 people in a team. The ideal team would consist
                    of one or two software developers, a designer, and one or
                    two business planners.
                </p>
                <h2 className="faq-header">Can I register without a team?</h2>
                <p className="faq-text">
                    Of course! If you are alone or if you only have 1 other
                    teammate, you can register and a facilitator from the Hub’s
                    organizing team will help you in finding more teammates.
                </p>
                <h2 className="faq-header">
                    Where will the Hackathon be held?
                </h2>
                <p className="faq-text">
                    The Hackathon will be in American University in Bulgaria’s
                    ABF Sports Hall, located on ul. Svoboda Bachvarova 12 in
                    Blagoevgrad.
                </p>
                <h2 className="faq-header">
                    How long will we have to develop our projects?
                </h2>
                <p className="faq-text">
                    The brainstorming process starts on Friday at 20:00 and you
                    will have until Sunday at 13:00 to submit your project. Make
                    sure you keep an eye on the clock!
                </p>
                <h2 className="faq-header">
                    Is there a theme for the Hackathon?
                </h2>
                <p className="faq-text">
                    Yes! However, it will be kept a secret until the Opening
                    Ceremony on Friday.
                </p>
                <h2 className="faq-header">
                    Can I start developing something in advance?
                </h2>
                <p className="faq-text">
                    We advise you to not start developing in advance, since the
                    project you will eventually develop has to be related to the
                    theme of the Hackathon, which is announced at the opening
                    ceremony. However, if you would like to research winning
                    projects from previous years, feel free! You can also start
                    brainstorming with your team well before the start of the
                    Hackathon.
                </p>
                <h2 className="faq-header">
                    What if I have an urgent question during the Hackathon?
                    Where can I ask?
                </h2>
                <p className="faq-text">
                    We will be setting up a Facebook group for the registered
                    participants. There, you can ask questions during the event.
                    In addition, the Hub members will be around at all times to
                    answer any questions that pop up.
                </p>
                <h2 className="faq-header">
                    Is there a specific technology or tech stack I need to use
                    for the Hackathon?
                </h2>
                <p className="faq-text">
                    No, there is not. You may use whatever you would like. Keep
                    in mind, however, that the judges tend to reward the
                    projects with more modern tech stacks more than others.
                </p>
            </div>
        </div>
    );
};

export default FaqSection;
