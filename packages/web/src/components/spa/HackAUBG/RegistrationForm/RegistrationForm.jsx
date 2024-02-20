import React, { useContext, useEffect, useState } from 'react'; // eslint-disable-line
import styles from './registration_form.module.css';
import { useForm } from 'react-hook-form';
//import { useState } from 'react';
import InputComponent from './InputComponent';
import axios from 'axios';
import { url } from '../../../../Global';
import { registerURL } from '../../../../Global';
//import { FsContext } from '../../../../feature_switches';

const RegistrationForm = () => {
    const {
        register,
        formState: { errors },
        handleSubmit,
        getValues,
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

    const onSubmit = () => {
        if (Object.keys(errors).length !== 0) {
            console.log(errors);
        } else {
            const values = getValues();
            const updatedValues = {};

            for (const [key, value] of Object.entries(values)) {
                if (value === 'true') {
                    updatedValues[key] = true;
                } else if (value === 'false') {
                    updatedValues[key] = false;
                } else {
                    updatedValues[key] = value;
                }
            }
            console.log(updatedValues);

            axios({
                method: 'post',
                url: registerURL,
                data: updatedValues,
            })
                .then(() => {
                    // setIsFormAvailable(true);
                    console.log('success');
                })
                .catch(() => {
                    // setIsFormAvailable(false);
                    console.log('failure');
                });
        }
    };

    const [displayTeam, setDisplayTeam] = useState(false);
    const [req, setReq] = useState('');
    const display = () => {
        if (getValues().team == 'true') {
            setDisplayTeam(true);
            setReq('Field is required');
        } else {
            setDisplayTeam(false);
            setReq('');
        }
    };

    return (
        <form className={styles.form} id="registration" onSubmit={handleSubmit(onSubmit)} onChange={display}>
            <div className={styles.form_container}>
                <div className={styles.form_row}>
                    <InputComponent
                        label="First Name*"
                        type="name"
                        required="true"
                        register={register}
                        name="first_name"
                        error={errors.first_name && errors.first_name.message}
                    />
                    <InputComponent
                        label="Last Name*"
                        type="name"
                        required="true"
                        register={register}
                        name="last_name"
                        error={errors.last_name && errors.last_name.message}
                    />
                </div>
                <div className={styles.form_row}>
                    <InputComponent
                        label="Email*"
                        type="email"
                        required="true"
                        register={register}
                        name="email"
                        error={errors.email && errors.email.message}
                    />
                    <InputComponent
                        label="Age*"
                        type="age"
                        required="true"
                        register={register}
                        name="age"
                        error={errors.age && errors.age.message}
                    />
                </div>
                <div className={styles.form_row}>
                    <InputComponent
                        label="Location*"
                        type="text"
                        required="Field is required"
                        register={register}
                        name="location"
                        error={errors.location && errors.location.message}
                    />
                    <InputComponent
                        label="Choose an School/University"
                        type="select"
                        required={false}
                        register={register}
                        values={[
                            'American University in Bulgaria',
                            'Sofia University',
                            'Technical University - Sofia',
                            'Plovdiv University',
                            'Other',
                        ]}
                        name="university"
                    />
                </div>
                <div className={styles.form_row}>
                    <InputComponent
                        label="Do you want to create a team*"
                        type="yesNo"
                        required="Field is required"
                        register={register}
                        setDisplay={display}
                        name="team"
                        error={errors.team && errors.team.message}
                    />
                    <InputComponent
                        label="What is the name of your team*"
                        type="text"
                        required={req}
                        register={register}
                        display={!displayTeam}
                        name="team_name"
                        error={errors.team_name && errors.team_name.message}
                    />
                </div>

                <div className={styles.form_row}>
                    <InputComponent
                        label="T-shirt size"
                        type="select"
                        required={false}
                        register={register}
                        values={['Small (S)', 'Medium (M)', 'Large (L)', 'Extra Large (XL)']}
                        name="tshirt_size"
                    />
                    <InputComponent
                        label="How did you find out about HackAUBG?*"
                        type="select"
                        required="Field is required"
                        register={register}
                        values={['University', 'Friends', 'I was on a previous edition of Hack AUBG']}
                        name="source_of_referral"
                        error={errors.source_of_referral && errors.source_of_referral.message}
                    />
                </div>

                <div className={styles.form_row}>
                    <InputComponent
                        label="What programming languages are you familiar with?*"
                        type="select"
                        required="Field is required"
                        register={register}
                        values={[
                            'Frontend Programming',
                            'Backend Programming',
                            'Programming in C#',
                            'Programming in Java',
                            'Programming in Python',
                            'Programming in Javascript',
                            "I don't have experience with any languages",
                            'Other',
                        ]}
                        name="programming_language"
                        error={errors.programming_language && errors.programming_language.message}
                    />
                    <InputComponent
                        label="What is your programming level?"
                        type="select"
                        required={false}
                        register={register}
                        values={[
                            'Beginner',
                            'Intermediate',
                            'Advanced',
                            'I am not participating as a programmer',
                            'Other',
                        ]}
                        name="programming_level"
                        error={errors.programming_level && errors.programming_level.message}
                    />
                </div>

                <div className={styles.form_row}>
                    <InputComponent
                        label="Have you participated in Hack AUBG before?"
                        type="yesNo"
                        required="Field is required"
                        register={register}
                        setDisplay={display}
                        name="has_participated_in_hackaubg"
                        error={errors.has_participated_in_hackaubg && errors.has_participated_in_hackaubg.message}
                    />
                    <InputComponent
                        label="Are you looking for an internship?"
                        type="yesNo"
                        required="Field is required"
                        register={register}
                        setDisplay={display}
                        name="has_internship_interest"
                        error={errors.has_internship_interest && errors.has_internship_interest.message}
                    />
                </div>

                <div className={styles.form_row}>
                    <InputComponent
                        label="Have you participated in other Hackathons?"
                        type="yesNo"
                        required="Field is required"
                        register={register}
                        setDisplay={display}
                        name="has_participated_in_hackathons"
                        error={errors.has_participated_in_hackathons && errors.has_participated_in_hackathons.message}
                    />
                    <InputComponent
                        label="Do you have previous coding experience?"
                        type="yesNo"
                        required="Field is required"
                        register={register}
                        setDisplay={display}
                        name="has_previous_coding_experience"
                        error={errors.has_previous_coding_experience && errors.has_previous_coding_experience.message}
                    />
                </div>

                <div className={styles.form_row}>
                    <InputComponent
                        label="Do you want to receive our newsletter with potential job offerings?"
                        type="yesNo"
                        required="Field is required"
                        register={register}
                        setDisplay={display}
                        name="newsletter_consent"
                        error={errors.newsletter_consent && errors.newsletter_consent.message}
                    />
                    <InputComponent
                        label="Agreement to share information with sponsors"
                        type="share_info_with_sponsors"
                        required={true}
                        register={register}
                        name="share_info_with_sponsors"
                        error={errors.share_info_with_sponsors && errors.share_info_with_sponsors.message}
                    />
                </div>
            </div>
            <input type="submit" />
        </form>
    );
    //  else return(<div>hello</div>);
};

export default RegistrationForm;
