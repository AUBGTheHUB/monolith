import React, { useContext, useEffect } from 'react'; // eslint-disable-line
import './registration_form.css';
import { useForm, SubmitHandler } from 'react-hook-form';
import { useState } from 'react';
import axios from 'axios';
import { url } from '../../../../Global';
import { BsExclamationCircleFill } from 'react-icons/bs';
import { FsContext } from '../../../../feature_switches';

const RegistrationForm = () => {
    const {
        register,
        handleSubmit,
        watch,
        formState: { errors },
    } = useForm();

    // const [loadingAnimation, setLoadingAnimation] = useState(false);
    // const [submitPressed, setSubmitPressed] = useState(false); // eslint-disable-line
    // const [submitButtonValue, setSubmitButtonValue] = useState('Register'); // eslint-disable-line
    // const [apiError, setApiError] = useState(false);
    // const [buttonMessage, setButtonMessage] = useState('');
    // const [disableTeamNameField, setDisableTeamNameField] = useState(true);
    // const [isFormAvailable, setIsFormAvailable] = useState(false);

    const checkRegistrationAvailability = () => {
        axios({
            method: 'get',
            url: url + '/api/hackathon/register/available',
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

    return (
        <form
            onSubmit={handleSubmit(data => {
                alert(JSON.stringify(data));
            })}>
            <label>Example</label>
            <input {...register('example')} defaultValue="test" />
            <label>ExampleRequired</label>
            <input {...register('exampleRequired', { required: true, maxLength: 10 })} />
            {errors.exampleRequired && <p>This field is required</p>}
            <input type="submit" />
        </form>
    );
};
