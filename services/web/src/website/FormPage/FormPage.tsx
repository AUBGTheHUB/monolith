import { FormProvider, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { RadioComponent } from '@/internal_library/RadioComponent/RadioComponent';
import { Button } from '@/components/ui/button';
import { InputComponent } from '@/internal_library/InputComponent/InputComponent';
import { DropdownComponent } from '@/internal_library/DropdownComponent/DropdownComponent';

const RADIO_OPTIONS = [
    { label: 'Yes', value: 'true' },
    { label: 'No', value: 'false' },
];

const TSHIRT_OPTIONS = [
    { label: 'Small (S)', value: 'Small (S)' },
    { label: 'Medium (M)', value: 'Medium (M)' },
    { label: 'Large (L)', value: 'Large (L)' },
];

const LEVEL_OPTIONS = [
    { label: 'Beginner', value: 'Beginner' },
    { label: 'Intermediate', value: 'Intermediate' },
    { label: 'Advanced', value: 'Advanced' },
];

const REFERRAL_OPTIONS = [
    { label: 'Friend', value: 'Friend' },
    { label: 'Social Media', value: 'Social Media' },
    { label: 'University Announcement', value: 'University Announcement' },
    { label: 'Other', value: 'Other' },
];

const PROGRAMMING_LANGUAGE_OPTIONS = [
    { label: 'JavaScript', value: 'JavaScript' },
    { label: 'Python', value: 'Python' },
    { label: 'Java', value: 'Java' },
    { label: 'C++', value: 'C++' },
    { label: 'C#', value: 'C#' },
    { label: 'Other', value: 'Other' },
];

const REGISTRATION_TYPE_OPTIONS = [
    { label: 'Individual', value: 'Individual' },
    { label: 'Team', value: 'Team' },
];

const UNIVERSITY_OPTIONS = [
    { label: 'American University in Bulgaria', value: 'American University in Bulgaria' },
    { label: 'Sofiiskiq', value: 'Sofiiskiq' },
    { label: 'Tehnicheski', value: 'Tehnicheski' },
    { label: 'Other', value: 'Other' },
];

const registrationSchema = z.object({
    name: z.string().min(1, 'Name is required'),
    email: z.string().email('Invalid email'),
    tshirt_size: z.enum(['Small (S)', 'Medium (M)', 'Large (L)']),
    university: z.string().min(1, 'University is required'),
    location: z.string().min(1, 'Location is required'),
    age: z.coerce.number().min(16, 'You must be at least 16 years old'),
    source_of_referral: z.string().optional(),
    programming_language: z.string().optional(),
    programming_level: z.enum(['Beginner', 'Intermediate', 'Advanced']),
    has_participated_in_hackaubg: z.enum(['true', 'false']).transform((val) => val === 'true'), //don't judge it's the only thing that worked lol
    has_internship_interest: z.enum(['true', 'false']).transform((val) => val === 'true'),
    has_participated_in_hackathons: z.enum(['true', 'false']).transform((val) => val === 'true'),
    has_previous_coding_experience: z.enum(['true', 'false']).transform((val) => val === 'true'),
    share_info_with_sponsors: z.enum(['true', 'false']).transform((val) => val === 'true'),
    registration_type: z.string(),
    is_admin: z.enum(['true', 'false']).transform((val) => val === 'true'),
    team_name: z.string().optional(),
});

export default function RegistrationForm() {
    const form = useForm<z.infer<typeof registrationSchema>>({
        resolver: zodResolver(registrationSchema),
        defaultValues: {
            name: '',
            email: '',
            tshirt_size: 'Small (S)',
            university: '',
            location: '',
            age: 16,
            source_of_referral: '',
            programming_language: '',
            programming_level: 'Beginner',
            has_participated_in_hackaubg: false,
            has_internship_interest: false,
            has_participated_in_hackathons: false,
            has_previous_coding_experience: false,
            share_info_with_sponsors: false,
            registration_type: '',
            is_admin: false,
            team_name: '',
        },
    });

    const onSubmit = (data: z.infer<typeof registrationSchema>) => {
        console.log('Form submitted:', data);
    };

    return (
        <FormProvider {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="bg-white">
                <InputComponent
                    control={form.control}
                    name="name"
                    label="Name"
                    type="text"
                    placeholder="Enter your name"
                />
                <InputComponent
                    control={form.control}
                    name="email"
                    label="Email"
                    type="email"
                    placeholder="Enter your email"
                />
                <DropdownComponent
                    control={form.control}
                    name="tshirt_size"
                    label="T-Shirt Size"
                    placeholder="Select your size"
                    items={TSHIRT_OPTIONS.map(({ label, value }) => ({ name: label, value }))}
                />
                <DropdownComponent
                    control={form.control}
                    name="university"
                    label="University"
                    placeholder="Select your university"
                    items={UNIVERSITY_OPTIONS.map(({ label, value }) => ({ name: label, value }))}
                />
                <InputComponent
                    control={form.control}
                    name="location"
                    label="Location:"
                    type="text"
                    placeholder="Enter your location"
                />
                <InputComponent
                    control={form.control}
                    name="age"
                    label="Age"
                    type="number"
                    placeholder="Enter your age"
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
                    items={PROGRAMMING_LANGUAGE_OPTIONS.map(({ label, value }) => ({ name: label, value }))}
                />
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
                <RadioComponent
                    control={form.control}
                    name="is_admin"
                    options={RADIO_OPTIONS}
                    groupLabel="Are you an admin?"
                />
                <InputComponent
                    control={form.control}
                    name="team_name"
                    label="Team Name"
                    type="text"
                    placeholder="Enter your team name (optional)"
                />
                <Button type="submit" className="text-black border border-black">
                    Register
                </Button>
            </form>
        </FormProvider>
    );
}
