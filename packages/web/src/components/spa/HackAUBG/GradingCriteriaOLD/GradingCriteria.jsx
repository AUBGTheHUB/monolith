import React from 'react';
import './grading_criteria.css';

export const GradingCriteriaOLD = () => {
    return (
        <div className="grading-criteria-container" id="grading">
            <h1>GRADING CRITERIA</h1>
            <div className="grading-criteria-table">
                <div className="grading-criteria-column">
                    <h2>
                        PROJECT IDEA<br></br> (15 points)
                    </h2>
                    <p>Innovative idea and originality (7 points)</p>
                    <p>Market Research (6 points)</p>
                    <p>Usage of external data to verify the idea (2 points)</p>
                </div>
                <div className="grading-criteria-column">
                    <h2>
                        PROJECT REALIZATION<br></br> (30 points)
                    </h2>
                    <p>UI/UX Design (10 points)</p>
                    <p>Scalability (10 points)</p>
                    <p>Project deployment (6 points)</p>
                    <p>Structured git repository (4 points)</p>
                </div>
                <div className="grading-criteria-column">
                    <h2>
                        COMPLEXITY OF THE PROJECT<br></br> (40 points)
                    </h2>
                    <p>Code originality (15 points)</p>
                    <p>Suitable technology stack (10 points)</p>
                    <p>Clear coding style (10 points)</p>
                    <p>Security (5 points)</p>
                </div>
                <div className="grading-criteria-column">
                    <h2>
                        PRESENTATION<br></br> (15 points)
                    </h2>
                    <p>Coherency (5 points)</p>
                    <p>Clear explanation and defense of project ideas (5 points)</p>
                    <p>Demo (3 points)</p>
                    <p>Demonstration and explanation of the most complex feature of the project (2 points)</p>
                </div>
            </div>
        </div>
    );
};
