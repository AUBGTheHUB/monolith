import { z } from 'zod';

const baseSchema = z.object({
    first_name: z
        .string()
        .min(1, { message: 'First Name is required.' })
        .min(3, { message: 'First Name must be at least 3 characters long.' })
        .max(50, { message: 'First Name cannot exceed 50 characters.' })
        .regex(/^[a-zA-Z\u0400-\u04FF\s-]+$/, {
            message: `Name can only contain letters, spaces and '-'.`,
        }),

    last_name: z
        .string()
        .min(1, { message: 'Last Name is required.' })
        .min(3, { message: 'Last Name must be at least 3 characters long.' })
        .max(50, { message: 'Last Name cannot exceed 50 characters.' })
        .regex(/^[a-zA-Z\u0400-\u04FF\s-]+$/, {
            message: `Last Name can only contain letters, spaces and '-'.`,
        }),

    university: z.string().min(1, { message: 'University is required.' }),

    age: z.coerce
        .number({
            required_error: 'Age is required.',
            invalid_type_error: 'Age is required.',
        })
        .int({ message: 'Age must be a whole number.' })
        .min(16, { message: 'You must be at least 16 years old.' })
        .max(69, { message: 'Age cannot exceed 69.' }),

    email: z.string().min(1, { message: 'Email is required' }).email({ message: 'Invalid email format.' }),

    country: z.string().min(1, { message: 'Country is required.' }),

    address: z
        .string()
        .min(1, { message: 'Adress is required.' })
        .min(3, { message: 'Adress must be at least 3 characters long.' })
        .max(100, { message: 'Adress cannot exceed 100 characters.' }),

    team_option: z.enum(['has_code', 'create_team', 'join_team'], {
        required_error: 'Please choose an option.',
    }),
    team_code: z.string().trim().optional(),
    team_name: z.string().trim().max(50, { message: 'Team name cannot exceed 50 characters.' }).optional(),
    has_team: z.boolean({ required_error: 'Please choose an option.' }),

    primary_role: z.string().min(3, { message: 'Primary role is required.' }),
    alternative_role: z.string().min(3, { message: 'Alternative role is required.' }),
    rank: z.string().min(3, { message: 'Rank is required.' }),

    share_info_with_sponsors: z.boolean({ message: 'Please select an option.' }),
});

export const registrationSchema = baseSchema.superRefine((data, ctx) => {
    if (data.has_team && !data.team_name) {
        ctx.addIssue({
            code: z.ZodIssueCode.custom,
            path: ['team_name'],
            message: 'Team name is required.',
        });
    }

    if (
        data.primary_role &&
        data.alternative_role &&
        data.primary_role.toLowerCase() === data.alternative_role.toLowerCase()
    ) {
        ctx.addIssue({
            code: z.ZodIssueCode.custom,
            path: ['alternative_role'],
            message: 'Alternative role must be different from your primary role.',
        });
    }
});

export type TournamentRegistrationFormData = z.infer<typeof registrationSchema>;
