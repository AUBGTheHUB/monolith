import React, { useEffect } from 'react'; // eslint-disable-line
import './registration_form.css';
import { useForm } from 'react-hook-form';
import { useState } from 'react';

const RegistrationForm = () => {
    const {
        register,
        handleSubmit,
        setError,
        formState: { errors } // eslint-disable-line
    } = useForm({ mode: 'all' });

    const [loadingAnimation, setLoadingAnimation] = useState(false);
    const [submitPressed, setSubmitPressed] = useState(false);
    const [submitButtonValue, setSubmitButtonValue] = useState('register'); // eslint-disable-line
    const [apiError, setApiError] = useState(false);

    const onSubmit = (data) => {
        setLoadingAnimation(true);
        // send request to backend
        // if res is good
        // block submit button, notify that registration is successful
        setTimeout(() => {
            setLoadingAnimation(false);
            setSubmitButtonValue('MONTANA');
            console.log(data);
        }, 2000);

        setTimeout(() => {}, 2000);

        // axios
        //     .get()
        //     .then(() => {})
        //     .catch(() => {});

        // request failed
        setTimeout(() => {
            setLoadingAnimation(true);
            setError(
                'test',
                {
                    type: 'focus',
                    message: 'API FAILED'
                }
                // { shouldFocus: true }
            );
            console.log(errors);
            setLoadingAnimation(false);
            setApiError(true);
        }, 2000);
    }; // send data to api
    const onError = (data) => {
        console.log('ERROR', data);
    };

    // useEffect will always initialize this with the correct state
    const [buttonState, setButtonState] = useState(
        'hackaubg-register-btn disabled'
    );

    const checkButtonAvailability = () => {
        if (apiError) {
            setButtonState('hackaubg-register-btn disabled');
            return;
        } else if (Object.keys(errors).length != 0 && submitPressed) {
            setButtonState('hackaubg-register-btn error');
            return;
        }
        setButtonState('hackaubg-register-btn');
    };

    useEffect(checkButtonAvailability, [Object.keys(errors)]);

    const showButton = () => {
        if (loadingAnimation) {
            return (
                <input
                    type="submit"
                    value="LOADING"
                    className="hackaubg-register-btn"
                />
            );
        } else {
            return (
                <input
                    type="submit"
                    className={buttonState}
                    value={submitButtonValue}
                    onClick={() => {
                        setSubmitPressed(true);
                    }}
                />
            );
        }
    };

    return (
        <div className="registration-main">
            <h1>Register for HackAUBG 5.0</h1>
            <form
                action=""
                className="reg-form"
                onSubmit={handleSubmit(onSubmit, onError)}
            >
                {errors.test && <p>{errors.test.message}</p>}

                <fieldset className="from-personal-info">
                    <div className="send-info">
                        <label htmlFor="">
                            Full Name
                            <input
                                type="text"
                                {...register('fullname', {
                                    required: {
                                        value: true,
                                        message: 'This field is required'
                                    },
                                    minLength: {
                                        message: 'Minimum length is 4 symbols',
                                        value: 4
                                    },
                                    maxLength: {
                                        message: 'Maximum length is 50 symbols',
                                        value: 50
                                    },
                                    pattern: {
                                        value: /^[\t a-zA-Z]{4,}(?: [a-zA-Z]+){0,2}$/,
                                        message:
                                            'No special characters and trailing spaces'
                                    }
                                })}
                            />
                        </label>
                        <p>{errors.fullname?.message}</p>
                    </div>
                    <div className="send-info">
                        <label htmlFor="">
                            Email
                            <input
                                type="text"
                                {...register('email', {
                                    required: {
                                        value: true,
                                        message: 'This field is required'
                                    },
                                    pattern: {
                                        value: /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/i,
                                        message: 'Please enter valid email'
                                    },
                                    minLength: {
                                        message: 'Minimum length is 4 symbols',
                                        value: 4
                                    }
                                })}
                            />
                            <p>{errors.email?.message}</p>
                        </label>
                    </div>
                    <div className="send-info">
                        <label htmlFor="">
                            Age
                            <input
                                type="text"
                                {...register('age', {
                                    required: {
                                        value: true,
                                        message: 'This field is required'
                                    },
                                    minLength: {
                                        message: 'Minimum length is 2 symbols',
                                        value: 2
                                    },
                                    maxLength: {
                                        message: 'Maximum length is 3 symbols',
                                        value: 3
                                    }
                                    // pattern: {
                                    //     value: /^[\t a-zA-Z]{4,}(?: [a-zA-Z]+){0,2}$/,
                                    //     message:
                                    //         'No special characters and trailing spaces'
                                    // }
                                })}
                            />
                        </label>
                        <p>{errors.age?.message}</p>
                    </div>
                    <div className="send-info">
                        <label htmlFor="">
                            Location
                            <input
                                type="text"
                                {...register('location', {
                                    required: {
                                        value: true,
                                        message: 'This field is required'
                                    },
                                    minLength: {
                                        message: 'Minimum length is 2 symbols',
                                        value: 2
                                    },
                                    maxLength: {
                                        message: 'Maximum length is 50 symbols',
                                        value: 50
                                    },
                                    pattern: {
                                        value: /^[\t a-zA-Z]{4,}(?: [a-zA-Z]+){0,2}$/,
                                        message:
                                            'No special characters and trailing spaces'
                                    }
                                })}
                            />
                        </label>
                        <p>{errors.location?.message}</p>
                    </div>
                    <div className="send-info">
                        <label className="radio-text">
                            School/University
                            <select
                                className="select"
                                {...register('university', {
                                    required: {
                                        value: true,
                                        message: 'This field is required'
                                    }
                                })}
                            >
                                <option value="" disabled selected>
                                    Choose a Location
                                </option>

                                <option value="AUBG">AUBG</option>
                                <option value="Sofia University">
                                    Sofia University
                                </option>
                                <option value="Technical University - Sofia">
                                    Technical University - Sofia
                                </option>
                                <option value="Plovdiv University">
                                    Plovdiv University
                                </option>
                                <option value="Other">Other</option>
                            </select>
                        </label>
                    </div>
                    <p>{errors.loc?.university}</p>

                    <div className="send-info">
                        <label className="column-right">
                            Do you want to receive our newsletter with potential
                            job offerings?
                        </label>
                        <div className="radio-select">
                            <div className="radio-btn">
                                <label>Yes</label>
                                <input
                                    {...register('JobOffers', {
                                        required: true
                                    })}
                                    type="radio"
                                    value="Yes"
                                    className="radio"
                                />
                            </div>
                            <div className="radio-btn">
                                <label>No</label>
                                <input
                                    {...register('JobOffers', {
                                        required: true
                                    })}
                                    type="radio"
                                    value=" No"
                                    className="radio"
                                />
                            </div>
                        </div>
                    </div>
                    <div className="send-info">
                        <label>
                            School/University
                            <select
                                name="university"
                                className="select"
                                required
                            >
                                <option value="">
                                    (Choose an institution)
                                </option>
                                <option value="1">AUBG</option>
                                <option value="2">Sofia University</option>
                                <option value="3">
                                    Technical University - Sofia
                                </option>
                                <option value="4">Plovdiv University</option>
                                <option value="5">
                                    Other (please specify)
                                </option>
                            </select>
                        </label>
                    </div>
                    {/*
                    
                   
                    <div className="send-info">
                        <label className="column-right">
                            T-shirt size
                            <select
                                name="shirt-size"
                                className="select"
                                required
                                onChange={handleInputChange}
                            >
                                <option value="">(Choose a size)</option>
                                <option value="1">Small (S)</option>
                                <option value="2">Medium (M)</option>
                                <option value="3">Large (L)</option>
                                <option value="4">Extra Large (XL)</option>
                            </select>
                        </label>
                    </div>
                    <div className="send-info">
                        <label className="column-left">
                            How did you find out about Hack AUBG?
                            <select
                                name="referrer"
                                className="select"
                                required
                                onChange={handleInputChange}
                            >
                                <option value="">(Choose one or more)</option>
                                <option value="1">University</option>
                                <option value="2">Friends</option>
                                <option value="3">
                                    I was on a previous edition of Hack AUBG
                                </option>
                                <option value="4">
                                    Other (please specify)
                                </option>
                            </select>
                        </label>
                    </div>
                    <div className="send-info">
                        <label className="column-right">
                            What are your strongest sides?
                            <select
                                name="skills"
                                className="select"
                                required
                                onChange={handleInputChange}
                            >
                                <option value="">(Choose one or more)</option>
                                <option value="1">Frontend Programming</option>
                                <option value="2">Backend Programming</option>
                                <option value="3">Programming in C#</option>
                                <option value="4">Programming in Java</option>
                                <option value="5">Programming in Python</option>
                                <option value="6">Marketing</option>
                                <option value="7">UI/UX</option>
                                <option value="8">Web development</option>
                                <option value="9">
                                    Other (please specify)
                                </option>
                            </select>
                        </label>
                    </div>
                    <div className="send-info">
                        <label htmlFor="">
                            What are your job interests?
                            <input
                                type="text"
                                name="job-interests"
                                placeholder="List the fields you are interested to work on"
                                required
                                onChange={handleInputChange}
                            />
                        </label>
                    </div>
                    <div className="send-info">
                        <label className="column-right">
                            What is your programming level?
                            <select
                                name="programming-level"
                                className="select"
                                required
                                onChange={handleInputChange}
                            >
                                <option value="">(Choose one or more)</option>
                                <option value="1">University</option>
                                <option value="2">Friends</option>
                                <option value="3">
                                    I was on a previous edition of Hack AUBG
                                </option>
                                <option value="4">
                                    Other (please specify)
                                </option>
                            </select>
                        </label>
                    </div>
                    <div className="send-info">
                        <label className="radio-text">
                            Do you have previous coding experience?
                        </label>
                        <div
                            className="radio-select"
                            required
                            onChange={handleInputChange}
                        >
                            <div className="radio-btn">
                                <label>Yes</label>
                                <input
                                    type="radio"
                                    name="joboffers"
                                    className="radio"
                                />
                            </div>
                            <div className="radio-btn">
                                <label>No</label>
                                <input
                                    type="radio"
                                    name="joboffers"
                                    className="radio"
                                />
                            </div>
                        </div>
                    </div>
                    <div className="send-info">
                        <label htmlFor="" className="column-right">
                            What is the name of your team?
                            <input
                                type="text"
                                name="team-name"
                                placeholder="Enter your team's name"
                                required
                            />
                        </label>
                    </div>
                    <div className="send-info">
                        <label className="radio-text">
                            Have you participated in Hack AUBG before?
                        </label>
                        <div className="radio-select">
                            <div
                                className="radio-btn"
                                required
                                onChange={handleInputChange}
                            >
                                <label>Yes</label>
                                <input
                                    type="radio"
                                    name="joboffers"
                                    className="radio"
                                />
                            </div>
                            <div className="radio-btn">
                                <label>No</label>
                                <input
                                    type="radio"
                                    name="joboffers"
                                    className="radio"
                                />
                            </div>
                        </div>
                    </div>
                    <div className="send-info">
                        <label className="radio-text">
                            Are you looking for an internship?
                        </label>
                        <div
                            className="radio-select"
                            required
                            onChange={handleInputChange}
                        >
                            <div className="radio-btn">
                                <label>Yes</label>
                                <input
                                    type="radio"
                                    name="joboffers"
                                    className="radio"
                                />
                            </div>
                            <div className="radio-btn">
                                <label>No</label>
                                <input
                                    type="radio"
                                    name="joboffers"
                                    className="radio"
                                />
                            </div>
                        </div>
                    </div>
                    <div className="send-info">
                        <label className="radio-text">
                            Have you participated in other hackathons?
                        </label>
                        <div
                            className="radio-select"
                            required
                            onChange={handleInputChange}
                        >
                            <div className="radio-btn">
                                <label>Yes</label>
                                <input
                                    type="radio"
                                    name="joboffers"
                                    className="radio"
                                />
                            </div>
                            <div className="radio-btn">
                                <label>No</label>
                                <input
                                    type="radio"
                                    name="joboffers"
                                    className="radio"
                                />
                            </div>
                        </div>
                    </div>
                    <div className="send-info">
                        <label className="radio-text">
                            Do you want to share you info with sponsors?
                        </label>
                        <div
                            className="radio-select"
                            required
                            onChange={handleInputChange}
                        >
                            <div className="radio-btn">
                                <label>Yes</label>
                                <input
                                    type="radio"
                                    name="joboffers"
                                    className="radio"
                                />
                            </div>
                            <div className="radio-btn">
                                <label>No</label>
                                <input
                                    type="radio"
                                    name="joboffers"
                                    className="radio"
                                />
                            </div>
                        </div>
                    </div>
                    <div className="send-info">
                        <label className="radio-text">
                            Do you have previous coding experience?
                        </label>
                        <div
                            className="radio-select"
                            required
                            onChange={handleInputChange}
                        >
                            <div className="radio-btn">
                                <label>Yes</label>
                                <input
                                    type="radio"
                                    name="joboffers"
                                    className="radio"
                                />
                            </div>
                            <div className="radio-btn">
                                <label>No</label>
                                <input
                                    type="radio"
                                    name="joboffers"
                                    className="radio"
                                />
                            </div>
                        </div>
                    </div>
                    <div className="send-info">
                        <label className="column-right">
                            Do you want to receive our newsletter with potential
                            job offerings?
                        </label>
                        <div
                            className="radio-select"
                            required
                            onChange={handleInputChange}
                        >
                            <div className="radio-btn">
                                <label>Yes</label>
                                <input
                                    type="radio"
                                    name="joboffers"
                                    className="radio"
                                />
                            </div>
                            <div className="radio-btn">
                                <label>No</label>
                                <input
                                    type="radio"
                                    name="joboffers"
                                    className="radio"
                                />
                            </div>
                        </div>
                    </div> */}
                </fieldset>
                {/* <button className="register-btn">Register</button> */}
                {/* <button
                    className="register-btn"
                    type="button"
                    onClick={() => {}}
                >
                    Register
                </button> */}
                {showButton()}
            </form>
        </div>
    );
};

export default RegistrationForm;
