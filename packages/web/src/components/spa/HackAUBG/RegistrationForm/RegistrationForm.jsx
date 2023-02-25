import React from 'react';
import './registration_form.css';

const RegistrationForm = () => {
    return (
        <div className="registration-main">
            <h1>Register for HackAUBG 5.0</h1>
            <form action="" className="reg-form">
                <fieldset className="from-personal-info">
                    <div className="send-info">
                        <label htmlFor="">
                            Full Name
                            <input
                                type="text"
                                name="full-name"
                                placeholder="Enter your name"
                                required
                            />
                        </label>
                    </div>
                    <div className="send-info">
                        <label htmlFor="">
                            Email
                            <input
                                type="email"
                                name="email"
                                placeholder="Enter your email"
                                required
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
                            />
                        </label>
                    </div>
                    <div className="send-info">
                        <label>
                            School/University
                            <select name="university" className="column-left">
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
                            <select name="shirt-size" className="column-right">
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
                            <select name="referrer" className="column-left">
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
                            <select name="skills" className="column-right">
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
                            />
                        </label>
                    </div>
                    <div className="send-info">
                        <label className="column-right">
                            What is your programming level?
                            <select
                                name="programming-level"
                                className="column-right"
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
                            Do you have a team?
                        </label>
                        <div className="radio-btn">
                            <label>Yes</label>
                            <input type="radio" name="team" />
                            <label className="radio-no">No</label>
                            <input type="radio" name="team" />
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
                        <div className="radio-btn">
                            <label>Yes</label>
                            <input type="radio" name="oldparticipant" />
                            <label className="radio-no">No</label>
                            <input type="radio" name="oldparticipant" />
                        </div>
                    </div>
                    <div className="send-info">
                        <label className="radio-text">
                            Are you looking for an internship?
                        </label>
                        <div className="radio-btn">
                            <label>Yes</label>
                            <input type="radio" name="internship" />
                            <label className="radio-no">No</label>
                            <input type="radio" name="internship" />
                        </div>
                    </div>
                    <div className="send-info">
                        <label className="radio-text">
                            Have you participated in other hackathons?
                        </label>
                        <div className="radio-btn">
                            <label>Yes</label>
                            <input type="radio" name="otherhackathon" />
                            <label className="radio-no">No</label>
                            <input type="radio" name="otherhackathon" />
                        </div>
                    </div>
                    <div className="send-info">
                        <label className="radio-text">
                            Do you want to share you info with sponsors?
                        </label>
                        <div className="radio-btn">
                            <label>Yes</label>
                            <input type="radio" name="shareinfo" />
                            <label className="radio-no">No</label>
                            <input type="radio" name="shareinfo" />
                        </div>
                    </div>
                    <div className="send-info">
                        <label className="radio-text">
                            Do you have previous coding experience?
                        </label>
                        <div className="radio-btn">
                            <label>Yes</label>
                            <input type="radio" name="experience" />
                            <label className="radio-no">No</label>
                            <input type="radio" name="experience" />
                        </div>
                    </div>
                    <div className="send-info">
                        <label className="column-right">
                            Do you want to receive our newsletter with potential
                            job offerings?
                        </label>
                        <div className="radio-btn">
                            <label>Yes</label>
                            <input type="radio" name="joboffers" />
                            <label className="radio-no">No</label>
                            <input type="radio" name="joboffers" />
                        </div>
                    </div>
                </fieldset>
                {/* <fieldset className="university column-left">
                    
                </fieldset>
                <fieldset className="shirt-size column-right">
                    
                </fieldset>
                <fieldset className="referrer column-left">
                    
                </fieldset>
                <fieldset className="skills column-right">
                    
                </fieldset>
                <fieldset className="job-interests column-left">

                </fieldset>
                <fieldset className="programming-level column-right">
                </fieldset>
                <fieldset className="team-section column-left">
                    
                    
                    
                    
                    
                    
                    
                    
                </fieldset> */}
                <button className="register-btn">Register</button>
            </form>
        </div>
    );
};

export default RegistrationForm;
