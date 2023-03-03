import React from 'react';
import { useRef, useState, useEffect } from 'react';
// import Alert from 'react-bootstrap/Alert';
import './registration_form.css';

const USER_REGEX = /^[a-zA-Z][\t a-zA-Z]{3,23}$/;

const RegistrationForm = () => {
    const userRef = useRef();
    const errRef = useRef();

    const [user, setUser] = useState('');
    const [validName, setValidName] = useState(false);
    const [setUserFocus] = useState(false);

    const [errMsg, setErrMsg] = useState('');
    // const [success, setSuccess] = useState(false);

    useEffect(() => {
        userRef.current.focus();
    }, []);

    useEffect(() => {
        const result = USER_REGEX.test(user);
        console.log(result);
        console.log(user);
        setValidName(result);
    }, [user]);

    useEffect(() => {
        setErrMsg('');
    }, [user]);

    //
    //     const handleInputChange = (event) => {
    //         const target = event.target;
    //         const value = target.value;
    //         const name = target.name;
    //
    //         setSuccess(0);
    //
    //         checkFormat(name, value);
    //
    //         setFormState({
    //             ...formState,
    //             [name]: value
    //         });
    //
    //         console.log(formState);
    //     };
    //
    //     function checkEmptyString(string) {
    //         return /^\s*$/.test(string);
    //     }
    //
    //     function checkEmail(string) {
    //         return /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(string);
    //     }
    //
    //     if (fullNameFormat !== 'field-correct' || emailFormat !== 'field-correct') {
    //         // setAlertShown('alert');
    //     }

    // const handleSubmit = () => {
    //     if (
    //         fullNameFormat !== 'field-correct' ||
    //         emailFormat !== 'field-correct'
    //     ) {
    //         setAlertShown('alert');
    //     } else {
    //         setAlertShown('alert-hidden');
    //         axios
    //             .post(url, formState)
    //             .then((res) => {
    //                 setSuccess(res.status);
    //                 console.log(res);
    //             })
    //             .catch((err) => {
    //                 setSuccess(500);
    //                 console.log(err);
    //             });
    //     }
    // };

    return (
        <div className="registration-main">
            <h1>Register for HackAUBG 5.0</h1>
            <p
                ref={errRef}
                className={errMsg ? 'errmsg' : 'offscreen'}
                aria-live="assertive"
            >
                {errMsg}
            </p>
            <form action="" className="reg-form">
                <fieldset className="from-personal-info">
                    <div className="send-info">
                        <label htmlFor="">
                            Full Name
                            <input
                                type="text"
                                id="fullname"
                                ref={userRef}
                                autoComplete="off"
                                onChange={(e) => setUser(e.target.value)}
                                placeholder="Enter your name"
                                required
                                aria-invalid={validName ? 'false' : 'true'}
                                aria-describedby="uidnote"
                                onFocus={() => setUserFocus(true)}
                                onBlur={() => setUserFocus}
                                // onChange={handleInputChange}
                            />
                        </label>
                    </div>
                    {/* <div className="send-info">
                        <label htmlFor="">
                            Email
                            <input
                                type="email"
                                name="email"
                                placeholder="Enter your email"
                                required
                                onChange={handleInputChange}
                            />
                        </label>
                    </div>
                    <div className="send-info">
                        <label htmlFor="">
                            Age
                            <input
                                type="number"
                                name="age"
                                placeholder="Enter your age"
                                min="15"
                                max="30"
                                required
                                onChange={handleInputChange}
                            />
                        </label>
                    </div>
                    <div className="send-info">
                        <label htmlFor="">
                            Location
                            <input
                                type="text"
                                name="location"
                                placeholder="Enter the place where you currently live"
                                required
                                onChange={handleInputChange}
                            />
                        </label>
                    </div>
                    <div className="send-info">
                        <label>
                            School/University
                            <select
                                name="university"
                                className="select"
                                required
                                onChange={handleInputChange}
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
                <button
                    className="register-btn"
                    type="button"
                    onClick={() => {
                        // handleSubmit();
                    }}
                >
                    Register
                </button>
            </form>
        </div>
    );
};

export default RegistrationForm;
