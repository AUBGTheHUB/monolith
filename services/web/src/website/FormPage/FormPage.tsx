import { FormProvider, useForm, useWatch } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { RadioComponent } from '@/internal_library/RadioComponent/RadioComponent';
import { Button } from '@/components/ui/button';
import { InputComponent } from '@/internal_library/InputComponent/InputComponent';
import { DropdownComponent } from '@/internal_library/DropdownComponent/DropdownComponent';

const RADIO_OPTIONS = [
    { label: 'Yes', value: true },
    { label: 'No', value: false },
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
    { label: 'Team', value: true },
    { label: 'Individual', value: false },
];

const UNIVERSITY_OPTIONS = [
    { label: 'American University in Bulgaria', value: 'American University in Bulgaria' },
    { label: 'Sofiiskiq', value: 'Sofiiskiq' },
    { label: 'Tehnicheski', value: 'Tehnicheski' },
    { label: 'Other', value: 'Other' },
];

// 1) Define all fields that are common to both admin and non-admin
//    (except for is_admin and team_name, which differ).
const baseSchema = z.object({
    name: z
        .string()
        .min(3, { message: 'Name must be at least 3 characters long.' })
        .max(50, { message: 'Name cannot exceed 50 characters.' })
        .regex(/^[a-zA-Z\s]+$/, {
            message: 'Name can only contain letters and spaces.',
        }),

    email: z.string().min(1, { message: 'Email is required' }).email({ message: 'Invalid email format.' }),

    tshirt_size: z.string().min(1, { message: 'Size is required.' }),
    university: z.string().min(1, { message: 'University is required.' }),

    location: z
        .string()
        .min(3, { message: 'Location must be at least 3 characters long.' })
        .max(100, { message: 'Location cannot exceed 100 characters.' }),

    age: z
        .number({ required_error: 'Age is required.' })
        .int({ message: 'Age must be a whole number.' })
        .min(16, { message: 'You must be at least 16 years old.' })
        .max(69, { message: 'Age cannot exceed 69.' }),

    source_of_referral: z.string().min(1, { message: 'Please select an option.' }),
    programming_language: z.string().min(1, { message: 'Please select an option.' }),
    programming_level: z.string().min(1, { message: 'Please select an option.' }),

    has_participated_in_hackaubg: z.boolean({ message: 'Please select an option.' }),
    has_internship_interest: z.boolean({ message: 'Please select an option.' }),
    has_participated_in_hackathons: z.boolean({ message: 'Please select an option.' }),
    has_previous_coding_experience: z.boolean({ message: 'Please select an option.' }),
    share_info_with_sponsors: z.boolean({ message: 'Please select an option.' }),
});

const adminSchema = baseSchema.extend({
    is_admin: z.literal(true),
    team_name: z.string().min(3, 'Team name must be at least 3 characters.'),
});

const nonAdminSchema = baseSchema.extend({
    is_admin: z.literal(false),
    team_name: z.string().optional(),
});

const mainAdminSchema = baseSchema
    .extend({
        is_admin: z.boolean({ message: 'Please select an option.' }),
        // Start by making team_name optional.
        team_name: z.string().optional(),
    })
    .superRefine((data, ctx) => {
        // If is_admin is true, then team_name must be provided and at least 3 characters.
        if (data.is_admin === true) {
            if (!data.team_name || data.team_name.trim().length < 3) {
                ctx.addIssue({
                    code: z.ZodIssueCode.too_small,
                    minimum: 3,
                    inclusive: true,
                    type: 'string',
                    message: 'Team name must be at least 3 characters.',
                    path: ['team_name'],
                });
            }
        }
    });

const adminNonAdminUnion = z.discriminatedUnion('is_admin', [adminSchema, nonAdminSchema]);

export const registrationSchema = z.union([mainAdminSchema, adminNonAdminUnion]);

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
            is_admin: undefined,
            team_name: '',
        },
    });

    const onSubmit = (data: z.infer<typeof registrationSchema>) => {
        console.log('Form submitted:', data);
    };

    const isAdmin = useWatch({
        control: form.control,
        name: 'is_admin',
    });

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
                    label="Location"
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
                    name="is_admin"
                    options={REGISTRATION_TYPE_OPTIONS}
                    groupLabel="Are you an admin?"
                />

                <InputComponent
                    control={form.control}
                    name="team_name"
                    label="Team Name"
                    type="text"
                    placeholder="Enter your team name"
                    disabled={isAdmin !== true}
                />
                <RadioComponent
                    control={form.control}
                    name="programming_level"
                    options={LEVEL_OPTIONS}
                    groupLabel="Programming Level"
                />
                <Button type="submit" className="text-black border border-black">
                    Register
                </Button>
            </form>
        </FormProvider>
    );
}
