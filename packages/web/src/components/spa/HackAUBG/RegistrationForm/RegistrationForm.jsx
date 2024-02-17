import React, { useContext, useEffect, useState } from 'react'; // eslint-disable-line
import './registration_form.css';
import { useForm } from 'react-hook-form';
//import { useState } from 'react';
import InputComponent from './InputComponent';
import axios from 'axios';
import { url } from '../../../../Global';
//import { FsContext } from '../../../../feature_switches';

const RegistrationForm = () => {
    const {
        register,
        formState: { errors },
        handleSubmit,
    } = useForm();

    // const [loadingAnimation, setLoadingAnimation] = useState(false);
    // const [submitPressed, setSubmitPressed] = useState(false); // eslint-disable-line
    // const [submitButtonValue, setSubmitButtonValue] = useState('Register'); // eslint-disable-line
    //const [apiError, setApiError] = useState(false);
    // const [buttonMessage, setButtonMessage] = useState('');
    // const [disableTeamNameField, setDisableTeamNameField] = useState(true);
    const [isFormAvailable, setIsFormAvailable] = useState(false);

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
    if (isFormAvailable) return null;

    // Callback version of watch.  It's your responsibility to unsubscribe when done.
    console.log(errors);
    const [displayTeam, setDisplayTeam] = useState(false);
    const display = value => {
        setDisplayTeam(value);
    };

    return (
        <form
            id="registration"
            onSubmit={handleSubmit(data => {
                console.log(data);
                alert(JSON.stringify(data));
            })}>
            <label>Example</label>
            <InputComponent label="First Name" type="name" required="true" register={register} name="first_name" />
            <InputComponent label="Last Name" type="name" required="true" register={register} name="last_name" />
            <InputComponent label="Email" type="email" required="true" register={register} name="email" />
            <InputComponent label="Age" type="age" required="true" register={register} name="age" />
            <InputComponent label="Location" type="text" required="true" register={register} name="location" />
            <InputComponent
                label="Do you have a team"
                type="yesNo"
                required="true"
                register={register}
                setDisplay={display}
                name="team_name"
            />
            <InputComponent
                label="What is the name of your team"
                type="text"
                required="true"
                register={register}
                display={displayTeam}
                name="team_name"
            />
            <InputComponent
                label="Choose an School/University"
                type="select"
                required={false}
                register={register}
                values={['AUBG', 'Sofia University', 'Technical University - Sofia', 'Plovdiv University', 'Other']}
                name="university"
            />
            <InputComponent
                label="T-shirt size"
                type="select"
                required={false}
                register={register}
                values={['Small (S)', 'Medium (M)', 'Large (L)', 'Extra Large (XL)']}
                name="tshirt_size"
            />
            <InputComponent
                label="How did you find out about HackAUBG?"
                type="select"
                required={true}
                register={register}
                values={['University', 'Friends', 'I was on a previous edition of Hack AUBG', 'other']}
                name="source_of_referral"
            />
            <InputComponent
                label="What programming languages are you familiar with?"
                type="select"
                required={true}
                register={register}
                values={[
                    'Frontend Programming',
                    'Backend Programming',
                    'Programming in C#',
                    'Programming in Java',
                    'Programming in Python',
                    'Programming in Javascript',
                    "I don't have experience with any languages",
                ]}
                name="programming_language"
            />
            <InputComponent
                label="What is your programming level?"
                type="select"
                required={true}
                register={register}
                values={['Beginner', 'Intermediate', 'Advanced', 'I am not participating as a programmer', 'Other']}
                name="programming_level"
            />
            <InputComponent
                label="Have you participated in Hack AUBG before?"
                type="yesNo"
                required="true"
                register={register}
                setDisplay={display}
                name="has_participated_in_hackaubg"
            />
            <InputComponent
                label="Are you looking for an internship?"
                type="yesNo"
                required="true"
                register={register}
                setDisplay={display}
                name="has_internship_interest"
            />
            <InputComponent
                label="Have you participated in other Hackathons?"
                type="yesNo"
                required="true"
                register={register}
                setDisplay={display}
                name="has_participated_in_hackathons"
            />
            <InputComponent
                label="Do you have previous coding experience?"
                type="yesNo"
                required="true"
                register={register}
                setDisplay={display}
                name="has_previous_coding_experience"
            />
            <InputComponent
                label="Do you want to receive our newsletter with potential job offerings?"
                type="yesNo"
                required="true"
                register={register}
                setDisplay={display}
                name="newsletter_consent"
            />
            <InputComponent
                label="Agreement to share information with sponsors"
                type="concent"
                required={true}
                register={register}
                name="share_info_with_sponsors"
            />
            <input type="submit" />
        </form>
    );
    //  else return(<div>hello</div>);
};

export default RegistrationForm;
