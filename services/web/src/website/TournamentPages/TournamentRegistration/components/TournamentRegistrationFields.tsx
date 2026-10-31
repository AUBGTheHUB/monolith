import { useEffect } from 'react';
import { Control, useFormContext, useWatch } from 'react-hook-form';
import { toast } from 'react-toastify';
import { TournamentRegistrationFormData } from '../schema';
import { InputComponent } from '@/internalLibrary/InputComponent/InputComponent';
import { DropdownComponent } from '@/internalLibrary/DropdownComponent/DropdownComponent';
import { RadioComponent } from '@/internalLibrary/RadioComponent/RadioComponent.tsx';
import { RADIO_OPTIONS, TEAM_OPTIONS, UNIVERSITY_OPTIONS, LEAGUE_ROLES } from '../constants';
import {
    ageControlStyles,
    formControlStyles,
    inputStyles,
    labelStyles,
    radioGroupStyles,
    radioOptionLabelStyles,
    radioQuestionStyles,
    selectContentStyles,
    teamRadioGroupStyles,
} from '../styles.ts';

type TournamentFieldsProps = {
    control: Control<TournamentRegistrationFormData>;
};

const toDropdownItems = (options: { label: string; value: string }[]) =>
    options.map(({ label, value }) => ({ name: label, value }));

export default function TournamentRegistrationFields({ control }: TournamentFieldsProps) {
    const { setValue, clearErrors } = useFormContext<TournamentRegistrationFormData>();

    const teamOption = useWatch({
        control: control,
        name: 'team_option',
    });

    useEffect(() => {
        if (teamOption === 'join_team') {
            toast('If you register as an individual participant, your participation is not guaranteed.', {
                toastId: 'join-team-warning',
                position: 'top-center',
                autoClose: 8000,
                icon: false,
                className:
                    "!bg-[#163B59] !text-[#90D5FF] !border-2 !border-[#C79B3B] !rounded-[12px] !font-['Rubik'] !font-bold !text-sm sm:!text-base !shadow-[0_0_20px_rgba(199,155,59,0.5)]",
                progressClassName: '!bg-[#C79B3B]',
            });
        }

        if (teamOption !== 'has_code') {
            clearErrors('team_code');
            setValue('team_code', '');
        }
        if (teamOption !== 'create_team') {
            clearErrors('team_name');
            setValue('team_name', '');
        }
    }, [teamOption, setValue, clearErrors]);

    return (
        <>
            <InputComponent
                control={control}
                name="first_name"
                label="First Name"
                type="text"
                placeholder="Type here..."
                labelClassName={labelStyles}
                inputClassName={inputStyles}
            />
            <InputComponent
                control={control}
                name="last_name"
                label="Last Name"
                type="text"
                placeholder="Type here..."
                labelClassName={labelStyles}
                inputClassName={inputStyles}
            />
            <InputComponent
                control={control}
                name="age"
                label="Age"
                type="number"
                placeholder=""
                labelClassName={labelStyles}
                inputClassName={`${inputStyles} ${ageControlStyles} [appearance:textfield] [&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none`}
            />
            <InputComponent
                control={control}
                name="email"
                label="Email"
                type="email"
                placeholder="Type here..."
                labelClassName={labelStyles}
                inputClassName={inputStyles}
            />
            <DropdownComponent
                control={control}
                name="university"
                label="University"
                placeholder=""
                dropdownLabelClassName={labelStyles}
                selectContentClassName={selectContentStyles}
                formControlClassName={formControlStyles}
                items={toDropdownItems(UNIVERSITY_OPTIONS)}
            />
            <InputComponent
                control={control}
                name="address"
                label="Address"
                type="text"
                placeholder="Type here..."
                labelClassName={labelStyles}
                inputClassName={inputStyles}
            />

            <RadioComponent
                control={control}
                name="team_option"
                options={TEAM_OPTIONS}
                groupLabel="How do you want to register?"
                groupClassName={radioQuestionStyles}
                radioGroupClassName={teamRadioGroupStyles}
                labelClassName={radioOptionLabelStyles}
            />

            {teamOption === 'has_code' && (
                <InputComponent
                    control={control}
                    name="team_code"
                    label="Enter your team code"
                    type="text"
                    placeholder="Type here..."
                    labelClassName={labelStyles}
                    inputClassName={inputStyles}
                />
            )}

            {teamOption === 'create_team' && (
                <InputComponent
                    control={control}
                    name="team_name"
                    label="What is your team name?"
                    type="text"
                    placeholder="Type here..."
                    labelClassName={labelStyles}
                    inputClassName={inputStyles}
                />
            )}

            <InputComponent
                control={control}
                name="rank"
                label="Rank in the game"
                type="text"
                placeholder="Type here..."
                labelClassName={labelStyles}
                inputClassName={inputStyles}
            />
            <DropdownComponent
                control={control}
                name="primary_role"
                label="Primary role"
                placeholder=""
                dropdownLabelClassName={labelStyles}
                selectContentClassName={selectContentStyles}
                formControlClassName={formControlStyles}
                items={toDropdownItems(LEAGUE_ROLES)}
            />
            <DropdownComponent
                control={control}
                name="alternative_role"
                label="Alternative role"
                placeholder=""
                dropdownLabelClassName={labelStyles}
                selectContentClassName={selectContentStyles}
                formControlClassName={formControlStyles}
                items={toDropdownItems(LEAGUE_ROLES)}
            />

            <RadioComponent
                control={control}
                name="share_info_with_sponsors"
                options={RADIO_OPTIONS}
                groupLabel="Do you agree to share your info with sponsors?"
                groupClassName={radioQuestionStyles}
                radioGroupClassName={radioGroupStyles}
                labelClassName={radioOptionLabelStyles}
            />
        </>
    );
}
