import React from 'react';
import styles from './verify_account.module.css';
import { FaRegWindowMinimize } from 'react-icons/fa';

export const VerifyAccount = () => {
    return (
        <div className={styles['verfication-container']}>
            <div className={styles['top-header']}>
                <div className={styles['svg-minimize']}>
                    <FaRegWindowMinimize />
                </div>
                <svg width="30" height="30" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="1" y="1" width="18" height="18" stroke="black" strokeWidth={'2'} />
                </svg>
                <svg width="32" height="32" viewBox="0 0 22 22" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path
                        d="M11.9775 11L19.3896 18.4229L18.4229 19.3896L11 11.9775L3.57715 19.3896L2.61035 18.4229L10.0225 11L2.61035 3.57715L3.57715 2.61035L11 10.0225L18.4229 2.61035L19.3896 3.57715L11.9775 11Z"
                        fill="black"
                    />
                </svg>
            </div>
            <div className={styles['sample-buttons-container']}>
                <div className={styles['sample-button']}>File</div>
                <div className={styles['sample-button-edit']}>Edit</div>
                <div className={styles['sample-button']}>Options</div>
                <div className={styles['sample-button']}>Help</div>
            </div>
            <div className={styles['verify-button-container']}>
                <div className={styles['verify-button']}>Verify</div>
            </div>
        </div>
    );
};

export default VerifyAccount;
