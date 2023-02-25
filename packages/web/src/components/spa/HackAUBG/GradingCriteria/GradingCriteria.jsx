import React from 'react';
import './grading_criteria.css';

export const GradingCriteria = () => {
    return (
        <div className="grading-criteria-table-container">
            <h1 className="grading-criteria-header">GRADING CRITERIA</h1>
            <div className="grading-criteria-table">
                <div className="grading-criteria-column">
                    <h2>
                        COMPLEXITY OF THE PROJECT<br></br> (20 points)
                    </h2>
                    <p>Scale (6 points)</p>
                    <p>Project Interface Design (3 points)</p>
                    <p>Relevance and Simplicity (8 points)</p>
                    <p>Scalability (3 points)</p>
                </div>
                <div className="grading-criteria-column">
                    <h2>
                        PROJECT REALIZATION<br></br> (10 points)
                    </h2>
                    <p>Scale (6 points)</p>
                    <p>Project Interface Design (3 points)</p>
                    <p>Relevance and Simplicity (8 points)</p>
                    <p>Scalability (3 points)</p>
                </div>
                <div className="grading-criteria-column">
                    <h2>
                        PROJECT IDEA<br></br> (10 points)
                    </h2>
                    <p>Scale (6 points)</p>
                    <p>Project Interface Design (3 points)</p>
                    <p>Relevance and Simplicity (8 points)</p>
                    <p>Scalability (3 points)</p>
                </div>
                <div className="grading-criteria-column">
                    <h2>
                        PRESENTATION<br></br> (10 points)
                    </h2>
                    <p>Scale (6 points)</p>
                    <p>Project Interface Design (3 points)</p>
                    <p>Relevance and Simplicity (8 points)</p>
                    <p>Scalability (3 points)</p>
                </div>
            </div>
        </div>
    );
};
