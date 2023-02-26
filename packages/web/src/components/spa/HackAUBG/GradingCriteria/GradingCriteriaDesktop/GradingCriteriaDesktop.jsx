import React from 'react';
import './grading_criteria_desktop.css';

export const GradingCriteriaDesktop = () => {
    return (
            <div className="grading-criteria-table-container-desktop" id="grading">
            <h1 className="grading-criteria-header-desktop">
                GRADING CRITERIA
            </h1>
            <table className="grading-criteria-table-desktop">
                <thead className="grading-criteria-thead-desktop">
                    <tr className=".grading-criteria-tr-desktop">
                        <th className=".grading-criteria-th-desktop">
                            COMPLEXITY OF THE PROJECT (20 points)
                        </th>
                        <th className=".grading-criteria-th-desktop">
                            PROJECT REALIZATION (10 points)
                        </th>
                        <th className=".grading-criteria-th-desktop">
                            PROJECT IDEA (10 points)
                        </th>
                        <th className=".grading-criteria-th-desktop">
                            PRESENTATION (10 points)
                        </th>
                    </tr>
                </thead>
                <tbody className="grading-criteria-tbody-desktop">
                    <tr className=".grading-criteria-tr-desktop">
                        <td className=".grading-criteria-td-desktop">
                            Scale (6 points)
                        </td>
                        <td className=".grading-criteria-td-desktop">
                            Scale (6 points)
                        </td>
                        <td className=".grading-criteria-td-desktop">
                            Scale (6 points)
                        </td>
                        <td className=".grading-criteria-td-desktop">
                            Scale (6 points)
                        </td>
                    </tr>
                    <tr className=".grading-criteria-tr-desktop">
                        <td className=".grading-criteria-td-desktop">
                            Project Interface Design (3 points)
                        </td>
                        <td className=".grading-criteria-td-desktop">
                            Project Interface Design (3 points)
                        </td>
                        <td className=".grading-criteria-td-desktop">
                            Project Interface Design (3 points)
                        </td>
                        <td className=".grading-criteria-td-desktop">
                            Project Interface Design (3 points)
                        </td>
                    </tr>
                    <tr className=".grading-criteria-tr-desktop">
                        <td className=".grading-criteria-td-desktop">
                            Relevance and Simplicity (8 points)
                        </td>
                        <td className=".grading-criteria-td-desktop">
                            Relevance and Simplicity (8 points)
                        </td>
                        <td className=".grading-criteria-td-desktop">
                            Relevance and Simplicity (8 points)
                        </td>
                        <td className=".grading-criteria-td-desktop">
                            Relevance and Simplicity (8 points)
                        </td>
                    </tr>
                    <tr className="border-bottom">
                        <td className=".grading-criteria-td-bottom-desktop">
                            Scalability (3 points)
                        </td>
                        <td className=".grading-criteria-td-bottom-desktop">
                            Scalability (3 points)
                        </td>
                        <td className=".grading-criteria-td-bottom-desktop">
                            Scalability (3 points)
                        </td>
                        <td className=".grading-criteria-td-bottom-desktop">
                            Scalability (3 points)
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    );
};
