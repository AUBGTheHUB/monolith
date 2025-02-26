import { FormProvider, useForm, useWatch } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { RadioComponent } from '@/internal_library/RadioComponent/RadioComponent';
import { Button } from '@/components/ui/button';
import { InputComponent } from '@/internal_library/InputComponent/InputComponent';
import { DropdownComponent } from '@/internal_library/DropdownComponent/DropdownComponent';
import { registrationSchema } from './schema';
import {
    LEVEL_OPTIONS,
    PROGRAMMING_LANGUAGE_OPTIONS,
    RADIO_OPTIONS,
    REFERRAL_OPTIONS,
    REGISTRATION_TYPE_OPTIONS,
    TSHIRT_OPTIONS,
    UNIVERSITY_OPTIONS,
} from './constants';

export default function RegistrationForm() {
    const form = useForm<z.infer<typeof registrationSchema>>({
        resolver: zodResolver(registrationSchema),
        defaultValues: {
            name: '',
            email: '',
            tshirt_size: '',
            university: '',
            location: '',
            age: 0,
            source_of_referral: '',
            programming_language: '',
            programming_level: undefined,
            has_participated_in_hackaubg: undefined,
            has_internship_interest: undefined,
            has_participated_in_hackathons: undefined,
            has_previous_coding_experience: undefined,
            share_info_with_sponsors: undefined,
            registration_type: undefined,
            team_name: '',
        },
    });

    const onSubmit = (data: z.infer<typeof registrationSchema>) => {
        console.log('Form submitted:', data);
    };

    const isAdmin = useWatch({
        control: form.control,
        name: 'registration_type',
    });

    return (
        <div className="w-full flex flex-col items-center font-mont bg-[#000912] relative text-gray-400">
            <div className="w-4/5 flex items-start mb-24 mt-16">
                <img src="/RegistrationForm/s.png" alt="" className="w-[1.6rem] mt-3" />
                <p className="text-white ml-5 tracking-[0.2em] text-3xl sm:text-4xl">REGISTER</p>
            </div>
            <div className="flex justify-center w-full">
                <FormProvider {...form}>
                    <form
                        onSubmit={form.handleSubmit(onSubmit)}
                        className="bg-[#000912] w-full max-w-5xl p-6 border border-gray-700 rounded-lg shadow-md"
                    >
                        <div className="">
                            <div>
                                <p className="text-lg font-semibold mb-2 mt-16">Personal Info</p>
                                <hr className="mb-8" />
                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                                    <InputComponent
                                        control={form.control}
                                        name="name"
                                        label="Name"
                                        type="text"
                                        placeholder="Enter your name"
                                    />
                                    <InputComponent
                                        control={form.control}
                                        name="age"
                                        label="Age"
                                        type="number"
                                        placeholder="Enter your age"
                                    />
                                    <InputComponent
                                        control={form.control}
                                        name="email"
                                        label="Email"
                                        type="email"
                                        placeholder="Enter your email"
                                    />
                                    <InputComponent
                                        control={form.control}
                                        name="location"
                                        label="Location"
                                        type="text"
                                        placeholder="Enter your location"
                                    />
                                    <DropdownComponent
                                        control={form.control}
                                        name="university"
                                        label="University"
                                        placeholder="Select your university"
                                        items={UNIVERSITY_OPTIONS.map(({ label, value }) => ({ name: label, value }))}
                                    />
                                </div>
                            </div>
                            <div>
                                <p className="text-lg font-semibold mt-16 mb-2">Participation</p>
                                <hr className="mb-8" />
                                <div className="grid ">
                                    <div className="grid grid-cols-2 gap-6">
                                        <DropdownComponent
                                            control={form.control}
                                            name="tshirt_size"
                                            label="T-Shirt Size"
                                            placeholder="Select your size"
                                            items={TSHIRT_OPTIONS.map(({ label, value }) => ({ name: label, value }))}
                                        />
                                        <DropdownComponent
                                            control={form.control}
                                            name="source_of_referral"
                                            label="Source of Referral"
                                            placeholder="How did you hear about us?"
                                            items={REFERRAL_OPTIONS.map(({ label, value }) => ({ name: label, value }))}
                                        />
                                        <DropdownComponent
                                            control={form.control}
                                            name="programming_language"
                                            label="Programming Language"
                                            placeholder="Select your preferred language"
                                            items={PROGRAMMING_LANGUAGE_OPTIONS.map(({ label, value }) => ({
                                                name: label,
                                                value,
                                            }))}
                                        />
                                    </div>

                                    <div className="grid grid-cols-1">
                                        <RadioComponent
                                            control={form.control}
                                            name="programming_level"
                                            options={LEVEL_OPTIONS}
                                            groupLabel="Programming Level"
                                        />
                                        <RadioComponent
                                            control={form.control}
                                            name="has_participated_in_hackaubg"
                                            options={RADIO_OPTIONS}
                                            groupLabel="Have you participated in HackAUBG before?"
                                        />
                                        <RadioComponent
                                            control={form.control}
                                            name="has_internship_interest"
                                            options={RADIO_OPTIONS}
                                            groupLabel="Are you interested in internships?"
                                        />
                                        <RadioComponent
                                            control={form.control}
                                            name="has_participated_in_hackathons"
                                            options={RADIO_OPTIONS}
                                            groupLabel="Have you participated in hackathons before?"
                                        />
                                        <RadioComponent
                                            control={form.control}
                                            name="has_previous_coding_experience"
                                            options={RADIO_OPTIONS}
                                            groupLabel="Do you have previous coding experience?"
                                        />
                                        <RadioComponent
                                            control={form.control}
                                            name="share_info_with_sponsors"
                                            options={RADIO_OPTIONS}
                                            groupLabel="Do you agree to share your info with sponsors?"
                                        />
                                        <RadioComponent
                                            control={form.control}
                                            name="registration_type"
                                            options={REGISTRATION_TYPE_OPTIONS}
                                            groupLabel="Enter registration type"
                                        />
                                        <InputComponent
                                            control={form.control}
                                            name="team_name"
                                            label="Team Name"
                                            type="text"
                                            placeholder="Enter your team name"
                                            disabled={isAdmin !== 'admin'}
                                        />
                                        <img src="/AwardsSection/line.svg" alt="Divider" className="w-full h-auto" />
                                    </div>
                                </div>
                            </div>
                            <div className="flex justify-start mt-4">
                                <Button
                                    type="submit"
                                    className="mt-10 text-white border-2 border-sky-600 rounded-full bg-transparent hover:bg-sky-600 transition-colors duration-500 hover:text-white"
                                >
                                    Participate now
                                </Button>
                            </div>
                        </div>
                    </form>
                </FormProvider>
            </div>
        </div>
    );
}
