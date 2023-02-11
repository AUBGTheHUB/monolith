import React from 'react';
import './grading_criteria_mobile.css';

export const GradingCriteriaMobile = () => {
    return (
        <div className="grading-criteria-table-container-mobile">
            <h1 className="grading-criteria-header-mobile">GRADING CRITERIA</h1>
            <table className="grading-criteria-table-mobile">
                <tbody>
                    <tr>
                        <td data-title="COMPLEXITY">COMPLEXITY</td>
                        <td>Scale (6 points)</td>
                        <td>Project Interface Design (3 points)</td>
                        <td>Relevance and Simplicity (8 points)</td>
                        <td id="lastDataEntry">Scalability (3 points)</td>
                    </tr>
                    <tr>
                        <td data-title="REALIZATION">REALIZATION</td>
                        <td>Scale (6 points)</td>
                        <td>Project Interface Design (3 points)</td>
                        <td>Relevance and Simplicity (8 points)</td>
                        <td id="lastDataEntry">Scalability (3 points)</td>
                    </tr>
                    <tr>
                        <td data-title="IDEA">IDEA</td>
                        <td>Scale (6 points)</td>
                        <td>Project Interface Design (3 points)</td>
                        <td>Relevance and Simplicity (8 points)</td>
                        <td id="lastDataEntry">Scalability (3 points)</td>
                    </tr>
                    <tr>
                        <td data-title="PRESENTATION">PRESENTATION</td>
                        <td>Scale (6 points)</td>
                        <td>Project Interface Design (3 points)</td>
                        <td>Relevance and Simplicity (8 points)</td>
                        <td id="lastDataEntry">Scalability (3 points)</td>
                    </tr>
                </tbody>
            </table>
        </div>
    );
};
