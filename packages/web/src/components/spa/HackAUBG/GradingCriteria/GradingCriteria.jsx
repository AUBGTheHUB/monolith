import styles from './garding_criteria.module.css';
import { FsContext } from '../../../../feature_switches';
import { useContext } from 'react';

export const GradingCriteria = () => {
    // eslint-disable-next-line
    const [featureSwitches, _] = useContext(FsContext);
    if (featureSwitches.GradeCrit) {
        return (
            <div className={styles.grading_criteria} id="grading">
                <h1 className={styles.grading_criteria_title}>Grading Criteria</h1>
                <div className={styles.grading_criteria_wrapper}>
                    <div className={styles.table_wrapper + ' ' + styles.left}>
                        <table className={styles.grading_criteria_table}>
                            <tr>
                                <th>PROJECT IDEA</th>
                                <th>Points</th>
                            </tr>
                            <tr>
                                <td>Innovative idea and originality</td>
                                <td className={styles.points}>8</td>
                            </tr>
                            <tr>
                                <td>Market Research</td>
                                <td className={styles.points}>5</td>
                            </tr>
                            <tr>
                                <td>Usage of external data to verify the idea</td>
                                <td className={styles.points}>2</td>
                            </tr>
                            <tr>
                                <td className={styles.total_points} colSpan={2}>
                                    Total: 15 points
                                </td>
                            </tr>
                        </table>
                    </div>
                    <span className={styles.line}></span>
                    <div className={styles.table_wrapper + ' ' + styles.right}>
                        <table className={styles.grading_criteria_table}>
                            <tr>
                                <th>PROJECT REALIZATION</th>
                                <th>Points</th>
                            </tr>
                            <tr>
                                <td>UI/UX Design</td>
                                <td className={styles.points}>10</td>
                            </tr>
                            <tr>
                                <td>Scalability</td>
                                <td className={styles.points}>10</td>
                            </tr>{' '}
                            <tr>
                                <td>Project deployment</td>
                                <td className={styles.points}>5</td>
                            </tr>{' '}
                            <tr>
                                <td>Structured git repository with documentation</td>
                                <td className={styles.points}>5</td>
                            </tr>
                            <tr>
                                <td className={styles.total_points} colSpan={2}>
                                    Total: 30 points
                                </td>
                            </tr>
                        </table>
                    </div>
                </div>
                <div className={styles.grading_criteria_wrapper}>
                    <div className={styles.table_wrapper + ' ' + styles.left}>
                        <table className={styles.grading_criteria_table}>
                            <tr>
                                <th>COMPLEXITY OF THE PROJECT</th>
                                <th>Points</th>
                            </tr>
                            <tr>
                                <td>Code originality</td>
                                <td className={styles.points}>15</td>
                            </tr>
                            <tr>
                                <td>Suitable technology stack</td>
                                <td className={styles.points}>10</td>
                            </tr>{' '}
                            <tr>
                                <td>Clear coding style</td>
                                <td className={styles.points}>10</td>
                            </tr>{' '}
                            <tr>
                                <td>Security</td>
                                <td className={styles.points}>5</td>
                            </tr>
                            <tr>
                                <td className={styles.total_points} colSpan={2}>
                                    Total: 40 points
                                </td>
                            </tr>
                        </table>
                    </div>
                    <span className={styles.line}></span>
                    <div className={styles.table_wrapper + ' ' + styles.right}>
                        <table className={styles.grading_criteria_table}>
                            <tr>
                                <th>PRESENTATION</th>
                                <th>Points</th>
                            </tr>
                            <tr>
                                <td>Coherency</td>
                                <td className={styles.points}>15</td>
                            </tr>
                            <tr>
                                <td>Clear explanation and defense of project ideas</td>
                                <td className={styles.points}>10</td>
                            </tr>{' '}
                            <tr>
                                <td>Demo</td>
                                <td className={styles.points}>10</td>
                            </tr>{' '}
                            <tr>
                                <td>Demonstration and explanation of the most complex feature of the project</td>
                                <td className={styles.points}>5</td>
                            </tr>
                            <tr>
                                <td className={styles.total_points} colSpan={2}>
                                    Total: 40 points
                                </td>
                            </tr>
                        </table>
                    </div>
                </div>
            </div>
        );
    } else {
        return (
            <p className={styles.grading_closed} id="registration">
                Grading criteria coming soon!
            </p>
        );
    }
};
