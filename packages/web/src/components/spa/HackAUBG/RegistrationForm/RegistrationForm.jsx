import React, { useEffect } from 'react'; // eslint-disable-line
import './registration_form.css';
import { useForm } from 'react-hook-form';
import { useState } from 'react';
import axios from 'axios';
import { url } from '../../../../Global';

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

    const makeRegistration = (data) => {
        axios({
            method: 'post',
            url: url + '/api/hackathon/register',
            headers: {
                'BEARER-TOKEN': localStorage.getItem('auth_token')
            },
            data: { ...data }
        })
            // eslint-disable-next-line no-unused-vars
            .then((res) => {
                console.log(res);
                // console.log('New registartion was added');
            })
            .catch((err) => {
                console.log(err);
                alert(err['response']['data']['data']['data']);
            });
    };

    const onSubmit = (data) => {
        setLoadingAnimation(true);
        // console.log(data);

        makeRegistration(data);
        // send request to backend
        // if res is good
        // block submit button, notify that registration is successful
        setTimeout(() => {
            setLoadingAnimation(false);
            setSubmitButtonValue('MONTANA');
            // console.log(data);
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
                                type="number"
                                {...register('age', {
                                    valueAsNumber: true,
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
                                    },
                                    pattern: {
                                        value: /^[0-9]+$/,
                                        message:
                                            'No special characters and trailing spaces'
                                    }
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
                        <label>
                            School/University
                            <select
                                className="select"
                                {...register('university', {
                                    required: true
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
                        <p>
                            {errors.university && (
                                <p className="error-text">
                                    University/School is required
                                </p>
                            )}
                        </p>
                    </div>
                    <div className="send-info">
                        <label>
                            T-shirt size
                            <select
                                className="select"
                                {...register('shirtsize', {
                                    required: true
                                })}
                            >
                                <option value="" disabled selected>
                                    Choose a size
                                </option>

                                <option value="Small (S)">Small (S)</option>
                                <option value="Medium (M)">Medium (M)</option>
                                <option value="Large (L)">Large (L)</option>
                                <option value="Extra Large (XL)">
                                    Extra Large (XL)
                                </option>
                            </select>
                        </label>
                        <p>
                            {errors.shirtsize && (
                                <p className="error-text">
                                    Shirt size is required
                                </p>
                            )}
                        </p>
                    </div>
                    <div className="send-info">
                        <label>
                            How did you find out about HackAUBG?
                            <select
                                className="select"
                                {...register('findout', {
                                    required: true
                                })}
                            >
                                <option value="" disabled selected>
                                    Choose one option
                                </option>

                                <option value="University">University</option>
                                <option value="Friends">Friends</option>
                                <option value="prevHackAUBG">
                                    I was on a previous edition of Hack AUBG
                                </option>
                                <option value="Other">Other</option>
                            </select>
                        </label>
                        <p>
                            {errors.findout && (
                                <p className="error-text">
                                    This field is required
                                </p>
                            )}
                        </p>
                    </div>
                    <div className="send-info">
                        <label>
                            What are your strongest sides?
                            <select
                                className="select"
                                {...register('strongsides', {
                                    required: true
                                })}
                            >
                                <option value="" disabled selected>
                                    Choose one option
                                </option>

                                <option value="Frontend Programming">
                                    Frontend Programming
                                </option>
                                <option value="Backend Programming">
                                    Backend Programming
                                </option>
                                <option value="Programming in C#">
                                    Programming in C#
                                </option>
                                <option value="Programming in Java">
                                    Programming in Java
                                </option>
                                <option value="Programming in Python">
                                    Programming in Python
                                </option>
                                <option value="Marketing">Marketing</option>
                                <option value="UI/UX">UI/UX</option>
                                <option value="Other">Other</option>
                            </select>
                        </label>
                        <p>
                            {errors.strongsides && (
                                <p className="error-text">
                                    This field is required
                                </p>
                            )}
                        </p>
                    </div>
                    <div className="send-info">
                        <label htmlFor="">
                            What are your job interests?
                            <input
                                type="text"
                                {...register('jobinterest', {
                                    required: {
                                        value: true,
                                        message: 'This field is required'
                                    },
                                    minLength: {
                                        message: 'Minimum length is 4 symbols',
                                        value: 4
                                    },
                                    maxLength: {
                                        message:
                                            'Maximum length is 100 symbols',
                                        value: 100
                                    }
                                })}
                            />
                        </label>
                        <p>{errors.jobinterest?.message}</p>
                    </div>
                    <div className="send-info">
                        <label>
                            What is your programming level?
                            <select
                                className="select"
                                {...register('level', {
                                    required: true
                                })}
                            >
                                <option value="" disabled selected>
                                    Choose one option
                                </option>

                                <option value="Beginner">Beginner</option>
                                <option value="Intermediate">
                                    Intermediate
                                </option>
                                <option value="Advanced">Advanced</option>
                                <option value="NotProgrammer">
                                    I am not participating as a programmer
                                </option>
                                <option value="Other">Other</option>
                            </select>
                        </label>
                        <p>
                            {errors.level && (
                                <p className="error-text">
                                    This field is required
                                </p>
                            )}
                        </p>
                    </div>
                    <div className="send-info">
                        <label className="column-right">
                            Do you have a team?
                        </label>
                        <div className="radio-select">
                            <div className="radio-btn">
                                <label>Yes</label>
                                <input
                                    {...register('DoYouHaveTeam', {
                                        required: true
                                    })}
                                    type="radio"
                                    value="True"
                                    className="radio"
                                />
                            </div>
                            <div className="radio-btn">
                                <label>No</label>
                                <input
                                    {...register('DoYouHaveTeam', {
                                        required: true
                                    })}
                                    type="radio"
                                    value="False"
                                    className="radio"
                                />
                            </div>
                        </div>
                        <p>
                            {errors.DoYouHaveTeam && (
                                <p className="error-text">
                                    This field is required
                                </p>
                            )}
                        </p>
                    </div>
                    <div className="send-info">
                        <label htmlFor="">
                            What is the name of your team
                            <input
                                type="text"
                                {...register('teamname', {
                                    required: {
                                        value: true,
                                        message: 'This field is required'
                                    },
                                    minLength: {
                                        message: 'Minimum length is 4 symbols',
                                        value: 4
                                    },
                                    maxLength: {
                                        message:
                                            'Maximum length is 100 symbols',
                                        value: 100
                                    }
                                })}
                            />
                        </label>
                        <p>{errors.teamname?.message}</p>
                    </div>
                    <div className="send-info">
                        <label className="column-right">
                            Have you participated in Hack AUBG before?
                        </label>
                        <div className="radio-select">
                            <div className="radio-btn">
                                <label>Yes</label>
                                <input
                                    {...register('prevHackAUBGParticipant', {
                                        required: true
                                    })}
                                    type="radio"
                                    value="True"
                                    className="radio"
                                />
                            </div>
                            <div className="radio-btn">
                                <label>No</label>
                                <input
                                    {...register('prevHackAUBGParticipant', {
                                        required: true
                                    })}
                                    type="radio"
                                    value="False"
                                    className="radio"
                                />
                            </div>
                        </div>
                        <p>
                            {errors.prevHackAUBGParticipant && (
                                <p className="error-text">
                                    This field is required
                                </p>
                            )}
                        </p>
                    </div>
                    <div className="send-info">
                        <label className="column-right">
                            Are you looking for an internship?
                        </label>
                        <div className="radio-select">
                            <div className="radio-btn">
                                <label>Yes</label>
                                <input
                                    {...register('LookingForInternship', {
                                        required: true
                                    })}
                                    type="radio"
                                    value="True"
                                    className="radio"
                                />
                            </div>
                            <div className="radio-btn">
                                <label>No</label>
                                <input
                                    {...register('LookingForInternship', {
                                        required: true
                                    })}
                                    type="radio"
                                    value="False"
                                    className="radio"
                                />
                            </div>
                        </div>
                        <p>
                            {errors.LookingForInternship && (
                                <p className="error-text">
                                    This field is required
                                </p>
                            )}
                        </p>
                    </div>
                    <div className="send-info">
                        <label className="column-right">
                            Have you participated in another Hackathons?
                        </label>
                        <div className="radio-select">
                            <div className="radio-btn">
                                <label>Yes</label>
                                <input
                                    {...register('otherHackParticipant', {
                                        required: true
                                    })}
                                    type="radio"
                                    value="True"
                                    className="radio"
                                />
                            </div>
                            <div className="radio-btn">
                                <label>No</label>
                                <input
                                    {...register('otherHackParticipant', {
                                        required: true
                                    })}
                                    type="radio"
                                    value="False"
                                    className="radio"
                                />
                            </div>
                        </div>
                        <p>
                            {errors.otherHackParticipant && (
                                <p className="error-text">
                                    This field is required
                                </p>
                            )}
                        </p>
                    </div>
                    <div className="send-info">
                        <label className="column-right">
                            Do you want to share you info with sponsors?
                        </label>
                        <div className="radio-select">
                            <div className="radio-btn">
                                <label>Yes</label>
                                <input
                                    {...register('shareInfoWithSponsors', {
                                        required: true
                                    })}
                                    type="radio"
                                    value="True"
                                    className="radio"
                                />
                            </div>
                            <div className="radio-btn">
                                <label>No</label>
                                <input
                                    {...register('shareInfoWithSponsors', {
                                        required: true
                                    })}
                                    type="radio"
                                    value="False"
                                    className="radio"
                                />
                            </div>
                        </div>
                        <p>
                            {errors.shareInfoWithSponsors && (
                                <p className="error-text">
                                    This field is required
                                </p>
                            )}
                        </p>
                    </div>
                    <div className="send-info">
                        <label className="column-right">
                            Do you have previous coding experience?
                        </label>
                        <div className="radio-select">
                            <div className="radio-btn">
                                <label>Yes</label>
                                <input
                                    {...register('prevExperience', {
                                        required: true
                                    })}
                                    type="radio"
                                    value="True"
                                    className="radio"
                                />
                            </div>
                            <div className="radio-btn">
                                <label>No</label>
                                <input
                                    {...register('prevExperience', {
                                        required: true
                                    })}
                                    type="radio"
                                    value="False"
                                    className="radio"
                                />
                            </div>
                        </div>
                        <p>
                            {errors.prevExperience && (
                                <p className="error-text">
                                    This field is required
                                </p>
                            )}
                        </p>
                    </div>
                    <div className="send-info">
                        <label className="column-right">
                            Do you want to receive our newsletter with potential
                            job offerings?{' '}
                        </label>
                        <div className="radio-select">
                            <div className="radio-btn">
                                <label>Yes</label>
                                <input
                                    {...register('JobOffers', {
                                        required: true
                                    })}
                                    type="radio"
                                    value="True"
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
                                    value="False"
                                    className="radio"
                                />
                            </div>
                        </div>
                        <p>
                            {errors.JobOffers && (
                                <p className="error-text">
                                    This field is required
                                </p>
                            )}
                        </p>
                    </div>
                </fieldset>

                {showButton()}
            </form>
        </div>
    );
};

export default RegistrationForm;
