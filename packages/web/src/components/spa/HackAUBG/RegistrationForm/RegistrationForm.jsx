import React from 'react';
import './registration_form.css';

const RegistrationForm = () => {
    return (
        <div className="registration-main">
            <h1>Register for HackAUBG 5.0</h1>
            <div className="registration-column-left">
                <p>Full name</p>
                <input type="text" />
                <p>Age</p>
                <input type="text" />
                <p>School/University </p>
                <input type="text" />
            </div>
            <div className="registration-column-right">
                <p>Email</p>
                <input type="email" />
                <p>Location</p>
                <input type="text" />
            </div>
        </div>
    );
};

export default RegistrationForm;
