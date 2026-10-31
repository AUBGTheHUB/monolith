import { z } from 'zod';

const ROLES = ['Jungle', 'Top Lane', 'Bot Lane', 'Support', 'Mid Lane'] as const;
const TEAM_OPTIONS = ['has_code', 'create_team', 'solo'] as const;

const NAME_REGEX = /^[\p{Script=Latin}\p{Script=Cyrillic}]+(?:[ '-][\p{Script=Latin}\p{Script=Cyrillic}]+)*$/u;

const nameField = (label: string) =>
    z
        .string({ required_error: `${label} is required.` })
        .trim()
        .min(2, { message: `${label} must be at least 2 characters long.` })
        .max(50, { message: `${label} cannot exceed 50 characters.` })
        .regex(NAME_REGEX, {
            message: `${label} can only contain letters, spaces, apostrophes and hyphens.`,
        });

const requiredString = (label: string, max?: number) => {
    let schema = z
        .string({ required_error: `${label} is required.` })
        .trim()
        .min(1, { message: `${label} is required.` });
    if (max) schema = schema.max(max, { message: `${label} cannot exceed ${max} characters.` });
    return schema;
};

const roleField = (label: string) =>
    z.enum(ROLES, {
        errorMap: () => ({ message: `${label} is required.` }),
    });

const baseSchema = z.object({
    full_name: nameField('Full name'),

    university: requiredString('University', 100),

    age: z.preprocess(
        (val) => (val === '' || val === null ? undefined : val),
        z.coerce
            .number({
                required_error: 'Age is required.',
                invalid_type_error: 'Age must be a number.',
            })
            .int({ message: 'Age must be a whole number.' })
            .min(16, { message: 'You must be at least 16 years old.' })
            .max(69, { message: 'Age cannot exceed 69.' }),
    ),

    email: z
        .string({ required_error: 'Email is required.' })
        .trim()
        .toLowerCase()
        .min(1, { message: 'Email is required.' })
        .max(254, { message: 'Email cannot exceed 254 characters.' })
        .email({ message: 'Invalid email format.' }),

    address: requiredString('Address', 100).min(3, {
        message: 'Address must be at least 3 characters long.',
    }),

    team_option: z.enum(TEAM_OPTIONS, {
        errorMap: () => ({ message: 'Please choose an option.' }),
    }),
    team_code: z.string().trim().optional(),
    team_name: z.string().trim().max(50, { message: 'Team name cannot exceed 50 characters.' }).optional(),

    primary_role: roleField('Primary role'),
    alternative_role: roleField('Alternative role'),

    rank: requiredString('Rank'),

    share_info_with_sponsors: z.boolean({
        required_error: 'Please select an option.',
        invalid_type_error: 'Please select an option.',
    }),
});

export const registrationSchema = baseSchema.superRefine((data, ctx) => {
    if (data.team_option === 'has_code' && !data.team_code) {
        ctx.addIssue({
            code: z.ZodIssueCode.custom,
            path: ['team_code'],
            message: 'Team code is required.',
        });
    }

    if (data.team_option === 'create_team' && !data.team_name) {
        ctx.addIssue({
            code: z.ZodIssueCode.custom,
            path: ['team_name'],
            message: 'Team name is required.',
        });
    }

    if (data.primary_role === data.alternative_role) {
        ctx.addIssue({
            code: z.ZodIssueCode.custom,
            path: ['alternative_role'],
            message: 'Alternative role must be different from your primary role.',
        });
    }
});
export type TournamentRegistrationFormData = z.infer<typeof baseSchema>;
