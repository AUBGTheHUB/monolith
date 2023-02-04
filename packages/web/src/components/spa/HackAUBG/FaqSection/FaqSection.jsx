import React from 'react';
import './faq_section.css';

export const FaqSection = () => {
    return (
        <div className="faq-container">
            <h1 className="faq">Frequently Asked Questions</h1>
            <h2 className="faq-header">
                What is the deadline for registering?
            </h2>
            <p className="faq-text">
                Registration is open until Friday, March 25th.
            </p>
            <h2 className="faq-header">Can I register without a team?</h2>
            <p className="faq-text">
                Yes! If your alone or if you have only 1 teammate you can
                register and a facilitator from the Hub organizing team will
                help you in finding more teammates. The wisest team-combo would
                be a developer or two, a designer, and one or two business
                planners.
            </p>
            <h2 className="faq-header">
                Can I start developing something in advance?
            </h2>
            <p className="faq-text">
                We would advise you not to begin developing anything, since the
                theme is what matters most when you decide on the project.
                However, you can definitely research winning projects from other
                hackathons and practice brainstorming and developing with your
                team
            </p>
            <h2 className="faq-header">Is there a theme for this hackathon?</h2>
        </div>
    );
};

export default FaqSection;
