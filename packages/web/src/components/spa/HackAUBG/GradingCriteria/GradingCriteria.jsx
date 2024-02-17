import styles from './garding_criteria.module.css';

export const GradingCriteria = () => {
    return (
        <div className={styles.grading_criteria}>
            <div className={styles.grading_criteria_row}>
                <div className={styles.grading_criteria_cell}>
                    <h2>PROJECT IDEA</h2>
                </div>
                <div className={styles.grading_criteria_cell}>
                    <h2>PROJECT REALIZATION</h2>
                </div>
            </div>
        </div>
    );
};
