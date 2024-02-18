import React, { useContext, useEffect } from 'react'; // eslint-disable-line

const InputComponent = ({ type, label, register, values, required, display, name, error }) => {
    let restrictions = '';
    let errorMessage = '';
    // if (display == false) {
    //     return null;
    // }
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
                <p style={{ color: 'red' }}>{error}</p>{' '}
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
                        max: { value: 99, message: 'Maximum age to participate is 99' },
                    })}></input>
                <p style={{ color: 'red' }}>{error}</p>{' '}
            </div>
        );
    } else if (type == 'yesNo') {
        return (
            <div>
                <label>{label}</label>
                <input
                    type="radio"
                    value="true"
                    {...register(name, {
                        required: 'Field is required',
                    })}></input>
                <input
                    type="radio"
                    value="false"
                    {...register(name, {
                        required: 'Field is required',
                    })}></input>
                <p style={{ color: 'red' }}>{error}</p>{' '}
            </div>
        );
    } else if (type === 'concent') {
        restrictions = 'true';
        errorMessage = 'You must agree <3';
        return (
            <div>
                <label>{label}</label>
                <input type="checkbox" {...register('concent', { required: 'Field is required' })}></input>
                <p style={{ color: 'red' }}>{error}</p>{' '}
            </div>
        );
    } else if (type == 'text') {
        return (
            <div disabled={display}>
                <label>{label}</label>
                <input
                    placeholder="Type here"
                    {...register(name, {
                        required: required,
                    })}></input>
                <p style={{ color: 'red' }}>{error}</p>{' '}
            </div>
        );
    } else if (type == 'select') {
        return (
            <div>
                <label>{label}</label>
                <select
                    {...register(name, {
                        required: required,
                        message: 'Field is required',
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
                <p style={{ color: 'red' }}>{error}</p>{' '}
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
