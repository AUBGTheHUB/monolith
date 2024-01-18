import React, { useContext, useEffect } from 'react'; // eslint-disable-line
import './registration_form.css';
import { useForm } from 'react-hook-form';
//import { useState } from 'react';
import InputComponent from './InputComponent';
//import axios from 'axios';
//import { url } from '../../../../Global';
//import { FsContext } from '../../../../feature_switches';

const RegistrationForm = () => {
    const { register, handleSubmit } = useForm();

    // const [loadingAnimation, setLoadingAnimation] = useState(false);
    // const [submitPressed, setSubmitPressed] = useState(false); // eslint-disable-line
    // const [submitButtonValue, setSubmitButtonValue] = useState('Register'); // eslint-disable-line
    // const [apiError, setApiError] = useState(false);
    // const [buttonMessage, setButtonMessage] = useState('');
    // const [disableTeamNameField, setDisableTeamNameField] = useState(true);
    // const [isFormAvailable, setIsFormAvailable] = useState(false);

    // const checkRegistrationAvailability = () => {
    //     axios({
    //         method: 'get',
    //         url: url + '/api/hackathon/register/available',
    //     })
    //         .then(() => {
    //             setIsFormAvailable(true);
    //         })
    //         .catch(() => {
    //             setIsFormAvailable(false);
    //         });
    // };

    // useEffect(() => {
    //     checkRegistrationAvailability();
    // }, []);
    // if(isFormAvailable)
    return (
        <form
            id="registration"
            onSubmit={handleSubmit(data => {
                console.log(data);
                alert(JSON.stringify(data));
            })}>
            <label>Example</label>
            <InputComponent label="First Name" type="firstName" required="true" register={register} />
            <InputComponent label="Last Name" type="lastName" required="true" register={register} />
            <InputComponent label="team?" type="yesNo" required="true" register={register} />
            <input type="submit" />
        </form>
    );
    //  else return(<div>hello</div>);
};

export default RegistrationForm;
