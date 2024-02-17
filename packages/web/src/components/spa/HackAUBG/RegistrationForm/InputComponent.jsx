import React, { useContext, useEffect } from 'react'; // eslint-disable-line

const InputComponent = ({ type, label, register, display, setDisplay, values, required, name }) => {
    let restrictions = '';
    let errorMessage = '';
    if (display == false) {
        return null;
    }
    if (type === 'name' || type == 'email') {
        if (type == 'email') {
            restrictions = /[a-zA-Z0-9._-]+@[a-zA-Z0-9]+.[a-zA-Z]{2,4}/;
            errorMessage = 'Please enter a valid email';
        } else {
            errorMessage = 'Name must be between 2 and 16 characters';
            restrictions = /(^[A-Za-z]{2,16})/;
        }
        return (
            <div>
                <label>{label}</label>
                <input
                    placeholder="Type here"
                    {...register(name, {
                        required: 'Field is required',
                        pattern: { value: restrictions, message: errorMessage },
                    })}></input>
            </div>
        );
    } else if (type == 'age') {
        errorMessage = 'Age must be a number';
        return (
            <div>
                <label>{label}</label>
                <input
                    type="number"
                    placeholder="Type here"
                    {...register(name, {
                        required: 'Field is required',
                        min: { value: 16, message: 'Minimum age to participate is 16' },
                    })}></input>
            </div>
        );
    } else if (type == 'yesNo') {
        if (label != 'Do you have a team') setDisplay = () => {};
        return (
            <div>
                <label>{label}</label>
                <input
                    type="radio"
                    name={label}
                    value="true"
                    {...register(name)}
                    onChange={() => {
                        setDisplay(true);
                    }}></input>
                <input
                    type="radio"
                    name={label}
                    value="false"
                    {...register(name)}
                    onChange={() => {
                        setDisplay(false);
                    }}></input>
            </div>
        );
    } else if (type === 'concent') {
        restrictions = 'true';
        errorMessage = 'You must agree <3';
        return (
            <div>
                <label>{label}</label>
                <input type="checkbox" {...register('concent', { required: true, message: errorMessage })}></input>
            </div>
        );
    } else if (type == 'text') {
        return (
            <div>
                <label>{label}</label>
                <input
                    placeholder="Type here"
                    {...register(name, {
                        required: 'Field is required',
                    })}></input>
            </div>
        );
    } else if (type == 'select') {
        return (
            <div>
                <label>{label}</label>
                <select
                    {...register(name, {
                        required: required,
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
            </div>
        );
    }

    return (
        <div>
            <label>{label}</label>
            <input type={type}></input>
        </div>
    );
};
export default InputComponent;
