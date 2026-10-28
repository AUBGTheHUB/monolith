import hextech from './images/hextech.png';

import ellipse1 from './images/ellipse1.png';
import line from './images/line.png';
import diamond from './images/diamond.png';
import { FormProvider, useForm, useWatch } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { RadioComponent } from '@/internalLibrary/RadioComponent/RadioComponent';
import { Button } from '@/components/ui/button';
import { InputComponent } from '@/internalLibrary/InputComponent/InputComponent';
import { DropdownComponent } from '@/internalLibrary/DropdownComponent/DropdownComponent';
import { registrationSchema, type RegistrationFormData } from './schema';
import { AGE_OPTIONS, COUNTRY_OPTIONS, RADIO_OPTIONS, TEAM_OPTIONS, UNIVERSITY_OPTIONS } from './constants';

import { useEffect, useState } from 'react';

import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import {
    titleStyles,
    sectionStyles,
    gearStyles,
    titleWhiteStyles,
    titleGoldStyles,
    labelStyles,
    inputStyles,
    radioGroupStyles,
    fieldGridStyles,
    submitButtonStyles,
    radioQuestionStyles,
    radioOptionLabelStyles,
} from './styles';

const toDropdownItems = (options: { label: string; value: string }[]) =>
    options.map(({ label, value }) => ({ name: label, value }));

export default function RegistrationForm() {
    const [fadeIn, setFadeIn] = useState(false);

    useEffect(() => {
        const timer = setTimeout(() => setFadeIn(true), 100);
        return () => clearTimeout(timer);
    }, []);

    const form = useForm<RegistrationFormData>({
        resolver: zodResolver(registrationSchema),
        defaultValues: {
            first_name: '',
            last_name: '',
            age: undefined,
            email: '',
            university: '',
            country: '',
            address: '',
            team_option: undefined,
            team_code: '',
            team_name: '',
            rank: '',
            primary_role: '',
            alternative_role: '',
            share_info_with_sponsors: undefined,
        },
    });

    const teamOption = useWatch({
        control: form.control,
        name: 'team_option',
    });

    useEffect(() => {
        if (teamOption === 'join_team') {
            toast('If you register as an individual participant, your participation is not guaranteed.', {
                position: 'top-center',
                autoClose: 8000,
                icon: false,
                className:
                    "!bg-[#163B59] !text-[#90D5FF] !border-2 !border-[#C79B3B] !rounded-[12px] !font-['Rubik'] !font-bold !text-lg !shadow-[0_0_20px_rgba(199,155,59,0.5)]",
                progressClassName: '!bg-[#C79B3B]',
            });
        }
    }, [teamOption]);

    useEffect(() => {
        if (teamOption !== 'has_code') {
            form.clearErrors('team_code');
            form.setValue('team_code', '');
        }
        if (teamOption !== 'create_team') {
            form.clearErrors('team_name');
            form.setValue('team_name', '');
        }
    }, [teamOption]);

    const onSubmit = (data: RegistrationFormData) => {
        console.log('Form data:', data);
        toast.success('Form submitted', {
            position: 'top-right',
            autoClose: 5000,
            className: 'bg-[#213a5a] text-[#a9ccf0] border border-[#c9a24a]',
        });
    };

    return (
        <section id="register" className={`${sectionStyles} ${fadeIn ? 'opacity-100' : 'opacity-0'}`}>
            <img src={hextech} alt="" className={gearStyles} />
            <img
                src={ellipse1}
                alt=""
                className="pointer-events-none absolute left-1/2 -translate-x-1/2 top-0 z-10 w-[95%] md:w-[85%] lg:w-[75%]"
            />
            <div className="z-10 flex items-center justify-center gap-5 md:gap-8 lg:gap-10 mt-16 md:mt-24 lg:mt-[170px] xl:mt-[190px] mb-6 md:mb-8 lg:mb-10">
                <img src={line} alt="" className="pointer-events-none w-20 md:w-40 lg:w-[218px]" />
                <img src={diamond} alt="" className="pointer-events-none w-[40px] md:w-[52px] lg:w-[63px]" />
                <img src={line} alt="" className="pointer-events-none w-20 md:w-40 lg:w-[218px] rotate-180" />
            </div>

            <h2 className={titleStyles}>
                <span className={titleWhiteStyles}>TOURNAMENT</span>
                <br />
                <span className={titleGoldStyles}>REGISTRATION</span>
            </h2>

            <p className="font-['Rubik'] font-light text-lg sm:text-xl md:text-[28px] lg:text-[36px] leading-[1.19] text-[#90D5FF] text-center w-full max-w-[892px] px-4 mb-6 md:mb-8 z-10">
                Fill in the form below to register for the tournament
            </p>

            <div className="relative z-10 w-11/12 max-w-[1220px] overflow-hidden bg-[#C79B3B] p-3 md:p-[22px]">
                <FormProvider {...form}>
                    <form
                        onSubmit={form.handleSubmit(onSubmit)}
                        className="relative isolate w-full rounded-[20px] px-6 py-10 md:px-24 md:py-16 flex flex-col"
                    >
                        <div className="absolute inset-0 -z-10 rounded-[20px] bg-[#163B59] blur-[20px]" />

                        <div className={fieldGridStyles}>
                            <InputComponent
                                control={form.control}
                                name="first_name"
                                label="First Name"
                                type="text"
                                placeholder="Type here..."
                                labelClassName={labelStyles}
                                inputClassName={inputStyles}
                            />
                            <InputComponent
                                control={form.control}
                                name="last_name"
                                label="Last Name"
                                type="text"
                                placeholder="Type here..."
                                labelClassName={labelStyles}
                                inputClassName={inputStyles}
                            />
                            <DropdownComponent
                                control={form.control}
                                name="age"
                                label="Age"
                                placeholder=""
                                dropdownLabelClassName={labelStyles}
                                selectContentClassName="bg-[#163B59] text-[#90D5FF] border-2 border-[#90D5FF] rounded-[5px] max-h-60"
                                formControlClassName="!w-[160px] md:!w-[208px] !h-12 md:!h-[57px] bg-transparent border-2 border-[#90D5FF] rounded-[5px] px-4 font-['Rubik'] text-lg md:text-2xl text-[#90D5FF] focus:outline-none focus:ring-2 focus:ring-[#C79B3B] [&_svg]:!h-6 [&_svg]:!w-6 md:[&_svg]:!h-8 md:[&_svg]:!w-8 [&_svg]:!opacity-100 [&_svg]:text-[#90D5FF] [&_svg]:stroke-[1.5]"
                                items={toDropdownItems(AGE_OPTIONS)}
                            />
                            <InputComponent
                                control={form.control}
                                name="email"
                                label="Email"
                                type="email"
                                placeholder="Type here..."
                                labelClassName={labelStyles}
                                inputClassName={inputStyles}
                            />
                            <DropdownComponent
                                control={form.control}
                                name="university"
                                label="University"
                                placeholder=""
                                dropdownLabelClassName={labelStyles}
                                selectContentClassName="bg-[#163B59] text-[#90D5FF] border-2 border-[#90D5FF] rounded-[5px] max-h-60"
                                formControlClassName="w-full max-w-[1005px] !h-12 md:!h-[57px] bg-transparent border-2 border-[#90D5FF] rounded-[5px] px-4 font-['Rubik'] text-lg md:text-2xl text-[#90D5FF] focus:outline-none focus:ring-2 focus:ring-[#C79B3B] [&_svg]:!h-6 [&_svg]:!w-6 md:[&_svg]:!h-8 md:[&_svg]:!w-8 [&_svg]:!opacity-100 [&_svg]:text-[#90D5FF] [&_svg]:stroke-[1.5]"
                                items={toDropdownItems(UNIVERSITY_OPTIONS)}
                            />
                            <DropdownComponent
                                control={form.control}
                                name="country"
                                label="Country"
                                placeholder=""
                                dropdownLabelClassName={labelStyles}
                                selectContentClassName="bg-[#163B59] text-[#90D5FF] border-2 border-[#90D5FF] rounded-[5px] max-h-60"
                                formControlClassName="w-full max-w-[1005px] !h-12 md:!h-[57px] bg-transparent border-2 border-[#90D5FF] rounded-[5px] px-4 font-['Rubik'] text-lg md:text-2xl text-[#90D5FF] focus:outline-none focus:ring-2 focus:ring-[#C79B3B] [&_svg]:!h-6 [&_svg]:!w-6 md:[&_svg]:!h-8 md:[&_svg]:!w-8 [&_svg]:!opacity-100 [&_svg]:text-[#90D5FF] [&_svg]:stroke-[1.5]"
                                items={toDropdownItems(COUNTRY_OPTIONS)}
                            />
                            <InputComponent
                                control={form.control}
                                name="address"
                                label="Address"
                                type="text"
                                placeholder="Type here..."
                                labelClassName={labelStyles}
                                inputClassName={inputStyles}
                            />

                            <RadioComponent
                                control={form.control}
                                name="team_option"
                                options={TEAM_OPTIONS}
                                groupLabel="How do you want to register?"
                                groupClassName={radioQuestionStyles}
                                radioGroupClassName={`${radioGroupStyles} xl:[&[role=radiogroup]]:!flex xl:[&[role=radiogroup]]:!justify-between xl:[&[role=radiogroup]]:!gap-10`}
                                labelClassName={radioOptionLabelStyles}
                            />

                            {teamOption === 'has_code' && (
                                <InputComponent
                                    control={form.control}
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
                                    control={form.control}
                                    name="team_name"
                                    label="What is your team name?"
                                    type="text"
                                    placeholder="Type here..."
                                    labelClassName={labelStyles}
                                    inputClassName={inputStyles}
                                />
                            )}

                            <InputComponent
                                control={form.control}
                                name="rank"
                                label="Rank in the game"
                                type="text"
                                placeholder="Type here..."
                                labelClassName={labelStyles}
                                inputClassName={inputStyles}
                            />
                            <InputComponent
                                control={form.control}
                                name="primary_role"
                                label="Primary role in the game"
                                type="text"
                                placeholder="Type here..."
                                labelClassName={labelStyles}
                                inputClassName={inputStyles}
                            />

                            <InputComponent
                                control={form.control}
                                name="alternative_role"
                                label="Alternative role in the game"
                                type="text"
                                placeholder="Type here..."
                                labelClassName={labelStyles}
                                inputClassName={inputStyles}
                            />

                            <RadioComponent
                                control={form.control}
                                name="share_info_with_sponsors"
                                options={RADIO_OPTIONS}
                                groupLabel="Do you agree to share your info with sponsors?"
                                groupClassName={radioQuestionStyles}
                                radioGroupClassName={radioGroupStyles}
                                labelClassName={radioOptionLabelStyles}
                            />
                        </div>

                        <div className="flex justify-end mt-10">
                            <Button type="submit" className={submitButtonStyles}>
                                SEND
                            </Button>
                        </div>
                    </form>
                </FormProvider>
            </div>

            <ToastContainer position="top-right" autoClose={5000} pauseOnHover draggable closeOnClick />
        </section>
    );
}
