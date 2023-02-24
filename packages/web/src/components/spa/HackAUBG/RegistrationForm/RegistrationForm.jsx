import React from 'react';
import './registration_form.css';

const RegistrationForm = () => {
    return (
        <div className="registration-main">
            <h1>Register for HackAUBG 5.0</h1>
            <form action="" className="reg-form">
                <fieldset className="personal-info">
                    <label htmlFor="">
                        Full Name
                        <input
                            type="text"
                            name="full-name"
                            placeholder="Enter your name"
                            required
                        />
                    </label>
                    <label htmlFor="">
                        Email
                        <input
                            type="email"
                            name="email"
                            placeholder="Enter your email"
                            required
                        />
                    </label>
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
                    <label htmlFor="">
                        Location
                        <input
                            type="text"
                            name="location"
                            placeholder="Enter the place where you currently live"
                            required
                        />
                    </label>
                </fieldset>
                <fieldset className="university">
                    <label>
                        School/University
                        <select name="university">
                            <option value="">(Choose an institution)</option>
                            <option value="1">AUBG</option>
                            <option value="2">Sofia University</option>
                            <option value="3">
                                Technical University - Sofia
                            </option>
                            <option value="4">Plovdiv University</option>
                            <option value="5">Other (please specify)</option>
                        </select>
                    </label>
                </fieldset>
                <fieldset className="shirt-size">
                    <label>
                        T-shirt size
                        <select name="shirt-size">
                            <option value="">(Choose a size)</option>
                            <option value="1">Small (S)</option>
                            <option value="2">Medium (M)</option>
                            <option value="3">Large (L)</option>
                            <option value="4">Extra Large (XL)</option>
                        </select>
                    </label>
                </fieldset>
                <fieldset>
                    <label>
                        How did you find out about Hack AUBG?
                        <select name="referrer">
                            <option value="">(Choose one or more)</option>
                            <option value="1">University</option>
                            <option value="2">Friends</option>
                            <option value="3">
                                I was on a previous edition of Hack AUBG
                            </option>
                            <option value="4">Other (please specify)</option>
                        </select>
                    </label>
                </fieldset>
                <fieldset className="skills">
                    <label>
                        What are your strongest sides?
                        <select name="skills">
                            <option value="">(Choose one or more)</option>
                            <option value="1">Frontend Programming</option>
                            <option value="2">Backend Programming</option>
                            <option value="3">Programming in C#</option>
                            <option value="4">Programming in Java</option>
                            <option value="5">Programming in Python</option>
                            <option value="6">Marketing</option>
                            <option value="7">UI/UX</option>
                            <option value="8">Web development</option>
                            <option value="9">Other (please specify)</option>
                        </select>
                    </label>
                </fieldset>
                <fieldset className="job-interests">
                    <label htmlFor="">
                        What are your job interests?
                        <input
                            type="text"
                            name="job-interests"
                            placeholder="List the fields you are interested to work on"
                            required
                        />
                    </label>
                </fieldset>
                <fieldset className="programming-level">
                    <label>
                        What is your programming level?
                        <select name="programming-level">
                            <option value="">(Choose one or more)</option>
                            <option value="1">University</option>
                            <option value="2">Friends</option>
                            <option value="3">
                                I was on a previous edition of Hack AUBG
                            </option>
                            <option value="4">Other (please specify)</option>
                        </select>
                    </label>
                </fieldset>
                <fieldset className="team-section">
                    <label>
                        Do you have a team?
                        <input type="radio" name="team" /> Yes
                        <input type="radio" name="team" /> No
                    </label>
                    <label htmlFor="">
                        What is the name of your team?
                        <input
                            type="text"
                            name="team-name"
                            placeholder="Enter your team's name"
                            required
                        />
                    </label>
                    <label>
                        Have you participated in Hack AUBG before?
                        <input type="radio" name="team" /> Yes
                        <input type="radio" name="team" /> No
                    </label>
                    <label>
                        Are you looking for an internship?
                        <input type="radio" name="team" /> Yes
                        <input type="radio" name="team" /> No
                    </label>
                    <label>
                        Have you participated in other hackathons?
                        <input type="radio" name="team" /> Yes
                        <input type="radio" name="team" /> No
                    </label>
                    <label>
                        Do you want to share you info with sponsors?
                        <input type="radio" name="team" /> Yes
                        <input type="radio" name="team" /> No
                    </label>
                    <label>
                        Do you have previous coding experience?
                        <input type="radio" name="team" /> Yes
                        <input type="radio" name="team" /> No
                    </label>
                    <label>
                        Do you want to receive our newsletter with potentila job
                        offerings?
                        <input type="radio" name="team" /> Yes
                        <input type="radio" name="team" /> No
                    </label>
                </fieldset>
                <button className="register-btn">Register</button>
            </form>
        </div>
    );
};

export default RegistrationForm;
