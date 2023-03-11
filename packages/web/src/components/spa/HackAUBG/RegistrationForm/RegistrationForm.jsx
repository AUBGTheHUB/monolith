import React, { useEffect } from 'react'; // eslint-disable-line
import './registration_form.css';
import { useForm } from 'react-hook-form';
import { useState } from 'react';
import axios from 'axios';
import { url } from '../../../../Global';
import { BsExclamationCircleFill } from 'react-icons/bs';

const RegistrationForm = () => {
    const {
        register,
        handleSubmit,
        formState: { errors } // eslint-disable-line
    } = useForm({ mode: 'all' });

    const [loadingAnimation, setLoadingAnimation] = useState(false);
    const [submitPressed, setSubmitPressed] = useState(false); // eslint-disable-line
    const [submitButtonValue, setSubmitButtonValue] = useState('Register'); // eslint-disable-line
    const [apiError, setApiError] = useState(false);
    const [buttonMessage, setButtonMessage] = useState('');
    const [disableTeamNameField, setDisableTeamNameField] = useState(true);
    const [isFormAvailable, setIsFormAvailable] = useState(false);

    const checkRegistrationAvailability = () => {
        axios({
            method: 'get',
            url: url + '/api/hackathon/register/available'
        })
            .then(() => {
                setIsFormAvailable(true);
            })
            .catch(() => {
                setIsFormAvailable(false);
            });
    };

    useEffect(() => {
        checkRegistrationAvailability();
    }, []);

    const registerMember = (data) => {
        axios({
            method: 'post',
            // TODO: Remove the url param when done with testing the endpoint
            // * this disables the mailing feature -> e.g. it won't send emails to random emails you use to test the registration with
            url: url + '/api/hackathon/register',
            data
        })
            // eslint-disable-next-line no-unused-vars
            .then((res) => {
                setLoadingAnimation(false);
                setApiError(false);
                console.log(res['response']['data']['message']);
            })
            .catch((err) => {
                setLoadingAnimation(false);
                setErrorMessage(err);
                setApiError(true); // put button in error state
                setSubmitButtonValue('Retry');
            });
    };

    function parseVars(data) {
        //getting all data from form and converting True/False string to boolean
        Object.entries(data).forEach((field) => {
            if (field[1] === 'True' || field[1] === 'False') {
                data[field[0]] = field[1] === 'True' ? true : false;
            }
        });
        return data;
    }

    //checking what error code we receive from the backend and outputing message depending on the code
    function setErrorMessage(err) {
        if (err['response']['status'] >= 500) {
            setButtonMessage('Something went wrong'); //add new message
        } else {
            setButtonMessage(err['response']['data']['message']);
        }
    }

    //send data to registerMember function
    const onSubmit = (data) => {
        setLoadingAnimation(true);
        data = parseVars(data);
        data = checkTeamname(data);
        registerMember(data);
    };

    // useEffect will always initialize this with the correct state
    const [buttonState, setButtonState] = useState(
        'hackaubg-register-btn disabled'
    );

    //handleDisabledFields will blur teamname inout field if they answer no
    const handleDisabledFields = (e) => {
        if (e.target.name === 'hasteam') {
            if (e.target.value === 'False') {
                setDisableTeamNameField(true);
            } else {
                setDisableTeamNameField(false);
            }
        }
    };
    //checks if user selected Yes/No on question about if they have team and if they do not have the teamname value is null
    function checkTeamname(data) {
        if (data.hasteam == false) {
            data.teamname = null;
        }
        return data;
    }

    //changes the button color and text depending on what is enetred in the form
    const checkButtonAvailability = () => {
        if (apiError) {
            setButtonState('hackaubg-register-btn error');
            return;
        } else if (!apiError) {
            if (Object.keys(errors).length != 0) {
                setButtonState('hackaubg-register-btn error');
                setSubmitPressed(false);
                setSubmitButtonValue('Retry');
                return;
            } else if (Object.keys(errors).length == 0 && submitPressed) {
                setButtonState('hackaubg-register-btn disabled');
                setSubmitButtonValue('Success');
                return;
            }
        }
        setButtonState('hackaubg-register-btn');
        setSubmitButtonValue('Submit');
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
    if (isFormAvailable) {
        return (
            <div className="registration-main" id="registration">
                <h1>Register for HackAUBG 5.0</h1>
                <form
                    action=""
                    className="reg-form"
                    onSubmit={handleSubmit(onSubmit)}
                    onChange={handleDisabledFields}
                >
                    <fieldset className="from-personal-info">
                        <div className="send-info">
                            <label>
                                Full Name
                                <input
                                    type="text"
                                    placeholder="Enter your name"
                                    {...register('fullname', {
                                        required: {
                                            value: true,
                                            message: '*This field is required'
                                        },
                                        minLength: {
                                            message:
                                                '*Minimum length is 4 characters',
                                            value: 4
                                        },
                                        maxLength: {
                                            message:
                                                'Maximum length is 50 characters',
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
                            <p className="error-msg">
                                {errors.fullname?.message}
                            </p>
                        </div>
                        <div className="send-info">
                            <label>
                                Email
                                <input
                                    type="text"
                                    placeholder="Enter your email"
                                    {...register('email', {
                                        required: {
                                            value: true,
                                            message: '*This field is required'
                                        },
                                        pattern: {
                                            value: /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/i,
                                            message: '*Please enter valid email'
                                        },
                                        minLength: {
                                            message:
                                                '*Minimum length is 4 characters',
                                            value: 4
                                        }
                                    })}
                                />
                                <p className="error-msg">
                                    {errors.email?.message}
                                </p>
                            </label>
                        </div>
                        <div className="send-info">
                            <label>
                                Age
                                <input
                                    type="number"
                                    placeholder="Enter your age"
                                    {...register('age', {
                                        required: {
                                            value: true,
                                            message: '*This field is required'
                                        },
                                        min: {
                                            message: 'Minimum age is 16',
                                            value: 16
                                        },
                                        max: {
                                            message:
                                                'Maximum length is 3 symbols',
                                            value: 99
                                        },
                                        pattern: {
                                            value: /^\d{2}$/,
                                            message:
                                                'No special characters and trailing spaces'
                                        },
                                        valueAsNumber: true
                                    })}
                                />
                            </label>
                            <p className="error-msg">{errors.age?.message}</p>
                        </div>
                        <div className="send-info">
                            <label>
                                Location
                                <input
                                    type="text"
                                    placeholder="Enter the place you currently live"
                                    {...register('location', {
                                        required: {
                                            value: true,
                                            message: '*This field is required'
                                        },
                                        minLength: {
                                            message:
                                                'Minimum length is 2 characters',
                                            value: 2
                                        },
                                        maxLength: {
                                            message:
                                                'Maximum length is 50 characters',
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
                            <p className="error-msg">
                                {errors.location?.message}
                            </p>
                        </div>
                        <div className="send-info">
                            <label>
                                School/University
                                <select
                                    defaultValue={'default'}
                                    className="select"
                                    {...register('university', {
                                        required: true
                                    })}
                                >
                                    <option value="default" disabled>
                                        Choose an School/University
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
                            <p className="error-msg">
                                {errors.university && (
                                    <p className="error-text">
                                        *University/School is required
                                    </p>
                                )}
                            </p>
                        </div>
                        <div className="send-info">
                            <label>
                                T-shirt size
                                <select
                                    className="select"
                                    defaultValue={'default'}
                                    {...register('shirtsize', {
                                        required: true
                                    })}
                                >
                                    <option value="default" disabled>
                                        Choose a size
                                    </option>

                                    <option value="Small (S)">Small (S)</option>
                                    <option value="Medium (M)">
                                        Medium (M)
                                    </option>
                                    <option value="Large (L)">Large (L)</option>
                                    <option value="Extra Large (XL)">
                                        Extra Large (XL)
                                    </option>
                                </select>
                            </label>
                            <p className="error-msg">
                                {errors.shirtsize && (
                                    <p className="error-text">
                                        *Shirt size is required
                                    </p>
                                )}
                            </p>
                        </div>
                        <div className="send-info">
                            <label>
                                How did you find out about HackAUBG?
                                <select
                                    className="select"
                                    defaultValue={'default'}
                                    {...register('heardaboutus', {
                                        required: true
                                    })}
                                >
                                    <option value="default" disabled>
                                        Choose one option
                                    </option>

                                    <option value="University">
                                        University
                                    </option>
                                    <option value="Friends">Friends</option>
                                    <option value="prevHackAUBG">
                                        I was on a previous edition of Hack AUBG
                                    </option>
                                    <option value="Other">Other</option>
                                </select>
                            </label>
                            <p className="error-msg">
                                {errors.heardaboutus && (
                                    <p className="error-text">
                                        *This field is required
                                    </p>
                                )}
                            </p>
                        </div>
                        <div className="send-info">
                            <label>
                                What are your strongest sides?
                                <select
                                    className="select"
                                    defaultValue={'default'}
                                    {...register('strongsides', {
                                        required: true
                                    })}
                                >
                                    <option value="default" disabled>
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
                            <p className="error-msg">
                                {errors.strongsides && (
                                    <p className="error-text">
                                        *This field is required
                                    </p>
                                )}
                            </p>
                        </div>
                        <div className="send-info">
                            <label>
                                What are your job interests?
                                <input
                                    type="text"
                                    placeholder="List the fields you are interested to work in"
                                    {...register('jobinterests', {
                                        required: {
                                            value: true,
                                            message: '*This field is required'
                                        },
                                        minLength: {
                                            message:
                                                '*Minimum length is 4 characters',
                                            value: 4
                                        },
                                        maxLength: {
                                            message:
                                                'Maximum length is 100 characters',
                                            value: 100
                                        }
                                    })}
                                />
                            </label>
                            <p className="error-msg">
                                {errors.jobinterests?.message}
                            </p>
                        </div>
                        <div className="send-info">
                            <label>
                                What is your programming level?
                                <select
                                    className="select"
                                    defaultValue={'default'}
                                    {...register('programminglevel', {
                                        required: true
                                    })}
                                >
                                    <option value="default" disabled>
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
                            <p className="error-msg">
                                {errors.programminglevel && (
                                    <p className="error-text">
                                        *This field is required
                                    </p>
                                )}
                            </p>
                        </div>
                        <div className="send-info">
                            <label className="radio-label">
                                Do you have a team?
                            </label>
                            <div className="radio-select">
                                <div className="radio-btn">
                                    <label>Yes</label>
                                    <input
                                        {...register('hasteam', {
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
                                        // onClick={teamToggle}
                                        {...register('hasteam', {
                                            required: true
                                        })}
                                        type="radio"
                                        value="False"
                                        className="radio"
                                    />
                                </div>
                            </div>
                            <p className="error-msg">
                                {errors.hasteam && (
                                    <p className="error-text">
                                        *This field is required
                                    </p>
                                )}
                            </p>
                        </div>
                        <div className="send-info">
                            <label>
                                What is the name of your team?
                                <input
                                    disabled={disableTeamNameField}
                                    placeholder={
                                        disableTeamNameField == false
                                            ? "Enter your team's name"
                                            : 'We will find you a team!'
                                    }
                                    type="text"
                                    {...register('teamname', {
                                        required: {
                                            value: !disableTeamNameField,
                                            message: '*This field is required'
                                        },
                                        minLength: {
                                            message:
                                                '*Minimum length is 4 characters',
                                            value: 4
                                        },
                                        maxLength: {
                                            message:
                                                'Maximum length is 100 characters',
                                            value: 100
                                        }
                                    })}
                                />
                            </label>
                            <p className="error-msg">
                                {errors.teamname?.message}
                            </p>
                        </div>
                        <div className="send-info">
                            <label className="radio-label">
                                Have you participated in Hack AUBG before?
                            </label>
                            <div className="radio-select">
                                <div className="radio-btn">
                                    <label>Yes</label>
                                    <input
                                        {...register(
                                            'prevhackaubgparticipation',
                                            {
                                                required: true
                                            }
                                        )}
                                        type="radio"
                                        value="True"
                                        className="radio"
                                    />
                                </div>
                                <div className="radio-btn">
                                    <label>No</label>
                                    <input
                                        {...register(
                                            'prevhackaubgparticipation',
                                            {
                                                required: true
                                            }
                                        )}
                                        type="radio"
                                        value="False"
                                        className="radio"
                                    />
                                </div>
                            </div>
                            <p className="error-msg">
                                {errors.prevhackaubgparticipation && (
                                    <p className="error-text">
                                        *This field is required
                                    </p>
                                )}
                            </p>
                        </div>
                        <div className="send-info">
                            <label className="radio-label">
                                Are you looking for an internship?
                            </label>
                            <div className="radio-select">
                                <div className="radio-btn">
                                    <label>Yes</label>
                                    <input
                                        {...register('wantinternship', {
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
                                        {...register('wantinternship', {
                                            required: true
                                        })}
                                        type="radio"
                                        value="False"
                                        className="radio"
                                    />
                                </div>
                            </div>
                            <p className="error-msg">
                                {errors.wantinternship && (
                                    <p className="error-text">
                                        *This field is required
                                    </p>
                                )}
                            </p>
                        </div>
                        <div className="send-info">
                            <label className="radio-label">
                                Have you participated in another Hackathons?
                            </label>
                            <div className="radio-select">
                                <div className="radio-btn">
                                    <label>Yes</label>
                                    <input
                                        {...register(
                                            'prevhackathonparticipation',
                                            {
                                                required: true
                                            }
                                        )}
                                        type="radio"
                                        value="True"
                                        className="radio"
                                    />
                                </div>
                                <div className="radio-btn">
                                    <label>No</label>
                                    <input
                                        {...register(
                                            'prevhackathonparticipation',
                                            {
                                                required: true
                                            }
                                        )}
                                        type="radio"
                                        value="False"
                                        className="radio"
                                    />
                                </div>
                            </div>
                            <p className="error-msg">
                                {errors.prevhackathonparticipation && (
                                    <p className="error-text">
                                        *This field is required
                                    </p>
                                )}
                            </p>
                        </div>
                        <div className="send-info">
                            <label className="radio-label">
                                Do you want to share you info with sponsors?
                            </label>
                            <div className="radio-select">
                                <div className="radio-btn">
                                    <label>Yes</label>
                                    <input
                                        {...register('shareinfowithsponsors', {
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
                                        {...register('shareinfowithsponsors', {
                                            required: true
                                        })}
                                        type="radio"
                                        value="False"
                                        className="radio"
                                    />
                                </div>
                            </div>
                            <p className="error-msg">
                                {errors.shareinfowithsponsors && (
                                    <p className="error-text">
                                        *This field is required
                                    </p>
                                )}
                            </p>
                        </div>
                        <div className="send-info">
                            <label className="radio-label">
                                Do you have previous coding experience?
                            </label>
                            <div className="radio-select">
                                <div className="radio-btn">
                                    <label>Yes</label>
                                    <input
                                        {...register('hasexperience', {
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
                                        {...register('hasexperience', {
                                            required: true
                                        })}
                                        type="radio"
                                        value="False"
                                        className="radio"
                                    />
                                </div>
                            </div>
                            <p className="error-msg">
                                {errors.hasexperience && (
                                    <p className="error-text">
                                        *This field is required
                                    </p>
                                )}
                            </p>
                        </div>
                        <div className="send-info">
                            <label className="radio-label">
                                Do you want to receive our newsletter with
                                potential job offerings?
                            </label>
                            <div className="radio-select">
                                <div className="radio-btn">
                                    <label>Yes</label>
                                    <input
                                        {...register('wantjoboffers', {
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
                                        {...register('wantjoboffers', {
                                            required: true
                                        })}
                                        type="radio"
                                        value="False"
                                        className="radio"
                                    />
                                </div>
                            </div>
                            <p className="error-msg">
                                {errors.wantjoboffers && (
                                    <p className="error-text">
                                        *This field is required
                                    </p>
                                )}
                            </p>
                        </div>
                    </fieldset>
                    {apiError == true && (
                        <p className="db-error-msg">
                            <BsExclamationCircleFill />
                            {buttonMessage}
                        </p>
                    )}
                    {showButton()}
                </form>
            </div>
        );
    }
    return <h1 className="reg-closed">Registration is closed</h1>;
};

export default RegistrationForm;
