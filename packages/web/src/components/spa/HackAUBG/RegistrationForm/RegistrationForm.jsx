import React from 'react';
import './registration_form.css';

const RegistrationForm = () => {
    return (
        <div className="registration-main">
            <h1>Register for HackAUBG 5.0</h1>
            <div className="registration-column-left">
                <p>Full name</p>
                <input type="text" placeholder="Enter your name" />
                <p>Age</p>
                <input type="text" placeholder="Enter your age" />
                <p>School/University </p>
                <input type="text" placeholder="Choose an institution" />
            </div>
            <div className="registration-column-right">
                <p>Email</p>
                <input type="email" placeholder="Enter your email" />
                <p>Location</p>
                <input
                    type="text"
                    placeholder="Enter the place where you currently live"
                />
            </div>
        </div>
    );
};

export default RegistrationForm;
