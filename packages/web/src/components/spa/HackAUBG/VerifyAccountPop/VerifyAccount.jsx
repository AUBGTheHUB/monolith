import React, { useState, useEffect } from 'react';
import styles from './verify_account.module.css';
import { FaRegWindowMinimize } from 'react-icons/fa';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import { verifyURL } from '../../../../Global';

export const VerifyAccount = ({ className, onSuccess }) => {
    const [jwtToken, setJwtToken] = useState('');
    const location = useLocation();
    const [buttonState, setButtonState] = useState(true);
    const [errorMsg, setErrorMsg] = useState('');
    useEffect(() => {
        const params = new URLSearchParams(location.search);
        setJwtToken(params.get('jwt_token'));
    }, []);

    const [error, setError] = useState(false);
    const [success, setSuccess] = useState(false);
    const [loading, setLoading] = useState(false);

    const handleVerifyClick = () => {
        setLoading(true);
        axios({
            method: 'get',
            url: verifyURL + `?jwt_token=${jwtToken}`,
        })
            .then(() => {
                setSuccess(true);
                setLoading(false);
                setButtonState(false);
                setTimeout(() => {
                    onSuccess();
                }, 3000);
            })

            .catch(err => {
                setError(true);
                console.log(err.response.status);
                if (err.response.status === 498) {
                    setErrorMsg('Invite link has expired');
                }

                setTimeout(() => {
                    setLoading(false);
                }, 3000);
            });
    };

    return (
        <div className={className}>
            <div className={`${styles['verfication-container']} ${error || success ? styles['message-shown'] : ''}`}>
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
                    <div className={styles['help-button-border']}>
                        <div className={styles['sample-button']}>Help</div>
                    </div>
                </div>
                <div
                    className={`${styles['verify-button-container']} ${
                        error || success ? styles['message-shown'] : ''
                    }`}>
                    <div
                        className={buttonState ? styles['verify-button'] : styles['verify-button-disabled']}
                        onClick={handleVerifyClick}>
                        Verify <span className={styles['button-message']}>participation</span>
                    </div>
                    {loading && <span className={styles['loader']}></span>}
                    {!loading && error && (
                        <div className={styles['error-message']}>
                            An error occured, please try again later! {errorMsg}
                        </div>
                    )}
                    {!loading && success && (
                        <div className={styles['success-message']}>You have been successfully verified!</div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default VerifyAccount;
