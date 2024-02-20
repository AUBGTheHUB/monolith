import React, { useContext, useEffect } from 'react'; // eslint-disable-line
import styles from './registration_form.module.css';

const InputComponent = ({ type, label, register, values, required, display, name, error }) => {
    let restrictions = '';
    let errorMessage = '';
    // if (display == false) {
    //     return null;
    // }
    if (type === 'name' || type == 'email') {
        if (type == 'email') {
            restrictions = /[a-zA-Z0-9._-]+@[a-zA-Z0-9]+.[a-zA-Z]{2,4}/;
            errorMessage = 'Please enter a valid email';
        } else {
            errorMessage = 'Name must be between 2 and 16 characters';
            restrictions = /(^[A-Za-z]{2,16})/;
        }
        return (
            <div className={styles.form_cell}>
                <label>{label}</label>
                <input
                    placeholder="Type here"
                    {...register(name, {
                        required: 'Field is required',
                        pattern: { value: restrictions, message: errorMessage },
                    })}></input>
                <div className={styles.error_msg}>
                    <p style={{ color: 'red' }}>{error}</p>
                </div>
            </div>
        );
    } else if (type == 'age') {
        errorMessage = 'Age must be a number';
        return (
            <div className={styles.form_cell}>
                <label>{label}</label>
                <input
                    type="number"
                    placeholder="Type here"
                    {...register(name, {
                        required: 'Field is required',
                        min: { value: 16, message: 'Minimum age to participate is 16' },
                        max: { value: 99, message: 'Maximum age to participate is 99' },
                    })}></input>
                <div className={styles.error_msg}>
                    <p style={{ color: 'red' }}>{error}</p>
                </div>
            </div>
        );
    } else if (type == 'yesNo') {
        return (
            <div className={styles.form_cell}>
                <label>{label}</label>
                <div className={styles.radio_group}>
                    <input
                        id={`${name}_true`}
                        type="radio"
                        value="true"
                        {...register(name, {
                            required: 'Field is required',
                        })}
                    />
                    <label htmlFor={`${name}_true`}>Yes</label>

                    <input
                        id={`${name}_false`}
                        type="radio"
                        value="false"
                        style={{ marginLeft: '15px' }}
                        {...register(name, {
                            required: 'Field is required',
                        })}
                    />
                    <label htmlFor={`${name}_false`}>No</label>
                </div>
                <div className={styles.error_msg}>
                    <p style={{ color: 'red' }}>{error}</p>
                </div>
            </div>
        );
    } else if (type === 'share_info_with_sponsors') {
        restrictions = 'true';
        errorMessage = 'You must agree <3';
        return (
            <div className={styles.form_cell}>
                <label>{label}</label>
                <input
                    type="checkbox"
                    {...register('share_info_with_sponsors', { required: 'Field is required' })}></input>
                <div className={styles.error_msg}>
                    <p style={{ color: 'red' }}>{error}</p>
                </div>
            </div>
        );
    } else if (type == 'text') {
        return (
            <div
                disabled={display}
                className={display ? `${styles.form_cell}` + ' ' + `${styles.disabled}` : `${styles.form_cell}`}>
                <label>{label}</label>
                <input
                    disabled={display}
                    placeholder="Type here"
                    {...register(name, {
                        required: required,
                    })}></input>
                <div className={styles.error_msg}>
                    <p style={{ color: 'red' }}>{error}</p>
                </div>
            </div>
        );
    } else if (type == 'select') {
        return (
            <div className={styles.form_cell}>
                <label>{label}</label>
                <select
                    {...register(name, {
                        required: required,
                        message: 'Field is required',
                    })}>
                    <option value="" selected disabled hidden>
                        Choose here
                    </option>
                    {values.map(el => (
                        <option value={el} key={el}>
                            {el}
                        </option>
                    ))}
                </select>
                <div className={styles.error_msg}>
                    <p style={{ color: 'red' }}>{error}</p>
                </div>
            </div>
        );
    }

    return (
        <div className={styles.form_cell}>
            <label>{label}</label>
            <input type={type}></input>
        </div>
    );
};
export default InputComponent;
