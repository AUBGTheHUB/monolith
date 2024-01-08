import React, { useContext, useEffect } from 'react'; // eslint-disable-line

const InputComponent = (label, type) => {
    let restrictions = '';
    let errorMessage = '';
    if (type === 'name') {
        restrictions = '/^[A-Za-z]{2,15}$/';
        errorMessage = 'Name must be between 2 and 15 characters';
    } else if (type == 'email') {
        restrictions = '/[a-zA-Z0-9._-]+@[a-zA-Z0-9]+.[a-zA-Z]{2,4}/';
        errorMessage = 'Please enter a valid email';
    } else if (type === 'tshirt') {
        restrictions = '/^(d*(?:M|X{0,2}[SsLl]))/i';
        errorMessage = 'Please use Universal Standart Sizing (XS,S,M,L...)';
    } else if (type === 'concent') {
        restrictions = 'true';
        errorMessage = 'You must agree <3';
    }
    return (
        <div>
            <label>{label}</label>
            <input type=""></input>
        </div>
    );
};
